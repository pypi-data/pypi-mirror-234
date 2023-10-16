import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import time
from shutil import copytree
from typing import Optional, Union

import click
from distributed import Client, Scheduler, SchedulerPlugin, UploadDirectory, Worker, WorkerPlugin
from rich import print

import coiled
from coiled.utils import logger

from .utils import CONTEXT_SETTINGS


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def prefect(ctx):
    """Prefect interface"""


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def worker(ctx):
    """Worker interface"""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--prefect-workspace",
    help="Name of the Prefect workspace.",
    required=True,
)
@click.option(
    "--prefect-key",
    help="API key for Prefect workspace, used to login Prefect workers.",
    default="",
)
@click.option(
    "--prefect-pool",
    default="default",
    help="Name of pool for Prefect worker.",
)
@click.option(
    "--prefect-work-queue",
    default="default",
    help="Name of Prefect work-queue for worker.",
)
@click.option(
    "--cluster-name",
    default=None,
    help="Name of Coiled cluster",
)
@click.option(
    "--n-workers",
    default=1,
    type=int,
    help="Number of Prefect workers to launch",
)
@click.option("--disable-adaptive", default=False, flag_value=True, help="Opt out of defaulting to an adaptive cluster")
@click.option(
    "--adaptive-min",
    default=0,
    type=int,
    help="Minimum workers in adaptive cluster configuration",
)
@click.option(
    "--adaptive-max",
    default=None,
    type=int,
    help="Maximum workers in adaptive cluster configuration",
)
@click.option(
    "--container",
    default=None,
    type=str,
    help="Docker image uri to use, ex: coiled/default:sha-2021.06.0",
)
def start(
    cluster_name: Optional[str],
    n_workers: int,
    prefect_workspace: str,
    prefect_work_queue: str,
    prefect_pool: str,
    disable_adaptive: bool,
    adaptive_min: int,
    adaptive_max: int,
    prefect_key: str = "",
    software: Optional[str] = None,
    container: Optional[str] = None,
):
    """
    Deploy Prefect Worker(s) on a Coiled cluster.

    This should be ran from the same code (and environment) used when
    deploying your Prefect flow/deployment. It will sync that directory's code
    to the VM(s) where the worker(s) will be running. Running the command from
    the desired Python environment also ensures all packages are synced to the
    Worker(s)/VM(s).
    """
    if not prefect_key:
        fn = os.path.expanduser(os.path.join("~", ".prefect", "profiles.toml"))
        try:
            import toml

            data = toml.load(fn)
            prefect_key = data["profiles"][data["active"]]["PREFECT_API_KEY"]
        except Exception:
            print(
                "[red]Missing API Key:[/red] Please log in to Prefect with\n\n"
                "    [green]prefect cloud login[/green]\n\n"
                "Or specify your Prefect API key with `--prefect-key <<KEY>>`"
            )
            sys.exit(1)
    cluster = coiled.Cluster(
        name=cluster_name,
        n_workers=n_workers - 1,  # One prefect worker on scheduler
        shutdown_on_close=False,
        scheduler_options={"idle_timeout": None},
        container=container,
        tags={"coiled-cluster-type": "prefect"},
    )
    client = cluster.get_client()

    _sync_local_storage(client)

    prefect_plugin = PrefectWorkerPlugin(
        cluster_name=cluster.name,  # type: ignore
        workspace=prefect_workspace,
        key=prefect_key,
        work_queue=prefect_work_queue,
        pool=prefect_pool,
    )
    client.register_worker_plugin(prefect_plugin, name="prefect-worker")
    client.register_scheduler_plugin(prefect_plugin, name="prefect-worker")

    if not disable_adaptive:
        adaptive_plugin = AdaptiveSchedulerPlugin(cluster.name, minimum=adaptive_min, maximum=adaptive_max)
        client.register_scheduler_plugin(adaptive_plugin)

    logger.info("Finished.")


worker.add_command(start, "start")
prefect.add_command(worker, "worker")


class AdaptiveSchedulerPlugin(SchedulerPlugin):
    """
    To persist cluster adaptivity, the ``Adaptive`` obj
    needs to stay alive. This does simply that, ``kwargs``
    is passed to ``coiled.Cluster.adapt`` and the result is
    stored in this plugin.
    """

    def __init__(self, name, **kwargs):
        self.kwargs = kwargs.copy()
        self.name = name

    async def start(self, scheduler) -> None:
        """Run when a new client connects"""
        if not hasattr(self, "adapt"):
            cluster = await coiled.Cluster(self.name, asynchronous=True)
            self.adapt = cluster.adapt(**self.kwargs)


class PrefectWorkerPlugin(SchedulerPlugin, WorkerPlugin):
    """
    A Scheduler/WorkerPlugin to run a Prefect worker on
    a Dask scheduler/worker as a subprocess.
    """

    proc: subprocess.Popen

    def __init__(
        self, cluster_name: str, workspace: str, key: str, work_queue: Optional[str] = None, pool: str = "default"
    ):
        self.cluster_name = cluster_name
        self.workspace = workspace
        self.key = key
        self.work_queue = work_queue
        self.pool = pool

    def start_prefect_worker(self, vm: Union[Worker, Scheduler]):
        subprocess.check_output(f"prefect cloud login -w {self.workspace} -k {self.key}".split())

        os.putenv("COILED__CLUSTER_NAME", self.cluster_name)
        os.putenv("PREFECT_EXTRA_ENTRYPOINTS", "coiled.extensions.prefect")

        cmd = "prefect worker start --type coiled-worker"
        cmd += f" --name {vm.name}" if hasattr(vm, "name") else ""  # type: ignore
        cmd += f" --pool {self.pool}" if self.pool else ""
        cmd += f" --work-queue {self.work_queue}" if self.work_queue else ""

        self.proc = subprocess.Popen(cmd.split())

        rc = self.proc.poll()
        if rc is not None:
            raise RuntimeError(f"Failed to start prefect worker, exit code: {rc}")

        # Monitor prefect worker doesn't die w/o us knowning about it.
        self._lock = threading.Lock()
        self._monitor_thread = threading.Thread(target=self.monitor_prefect_worker)
        self._monitor_thread.start()

    def stop_prefect_worker(self):
        with self._lock:
            self.proc.terminate()
            self.proc.wait()

    def monitor_prefect_worker(self):
        while True:
            with self._lock:
                rc = self.proc.poll()
            if rc is not None:
                if rc == 0:
                    break
                raise RuntimeError(f"Prefect worker died, exit code: {rc}")
            time.sleep(10)

    # SchedulerPlugin bridge
    async def start(self, scheduler: Scheduler):
        self.start_prefect_worker(scheduler)

    async def close(self):
        self.stop_prefect_worker()

    # WorkerPlugin bridge
    def setup(self, worker: Worker):
        self.start_prefect_worker(worker)

    def teardown(self, worker: Worker):
        self.stop_prefect_worker()


# TODO: PR to distributed to support UploadDirectory plugin for scheduler
# A proper implementation requires distributed>=2023.5.1 which is higher
# than prefect-dask's latest (0.2.4) allows: distributed<=2023.3.1,>=2022.5.0
# Ref: https://github.com/PrefectHQ/prefect-dask/blob/70a93dc6154e36782ea4b81151ce51ec447ceb1a/requirements.txt#L3
class UploadDirectorySchedulerPlugin(UploadDirectory, SchedulerPlugin):
    async def start(self, scheduler: Scheduler):
        # Remove when prefect-dask can be used w/ distributed>=2023.5.1
        scheduler.local_directory = "/tmp"  # type: ignore
        await self.setup(scheduler)


def _sync_local_storage(client: Client):
    logger.info("Syncing local storage to VMs...")
    # TODO: Hacky hack! - We're assuming LocalStorage for Prefect deployment here.
    #       To make the VMs look the same, we need to modify the output of UploadDirectory to
    #       the same path of the locally deployed workflow, assumed to be the cwd in this context.
    #       So we inject a file to echo the output location then copy files to same path on the VM
    #       as was found locally. Ideally, we could pass a destination dir to UploadDirectory.
    workflow_dir = pathlib.Path.cwd()  # Maybe CLI option, assumed running in same dir as workflow
    with tempfile.TemporaryDirectory() as tmpdir:
        copytree(str(workflow_dir), str(tmpdir), dirs_exist_ok=True)
        f = pathlib.Path(tmpdir).joinpath("__discover_location.py")
        f.write_text(
            """
import pathlib

def location():
    return pathlib.Path(__file__).parent
            """
        )
        upload_dir_plugin = UploadDirectory(str(tmpdir), restart=True, update_path=True)
        client.register_worker_plugin(upload_dir_plugin)

        upload_dir_plugin = UploadDirectorySchedulerPlugin(str(tmpdir), restart=True, update_path=True)
        client.register_scheduler_plugin(upload_dir_plugin)

    def copy_to_expected():
        """Running on workers, copy inital UploadDirectory of workflow code to same local path"""
        from __discover_location import location  # type: ignore

        # Copy Prefect workflow over to path that matches the local path it was deployed from
        # to match the LocalStorage
        copytree(str(location()), str(pathlib.Path(workflow_dir)), dirs_exist_ok=True)

    client.run(copy_to_expected)
    client.run_on_scheduler(copy_to_expected)
