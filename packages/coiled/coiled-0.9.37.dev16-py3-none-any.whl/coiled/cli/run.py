from __future__ import annotations

import io
import json
import os
import shlex
import subprocess
import sys
import time
from typing import Optional, Sequence

import click
import dask.config
from dask.base import tokenize
from dask.distributed import Client, get_worker
from dask.utils import parse_timedelta
from packaging.version import Version
from rich import print

import coiled
from coiled.compatibility import DISTRIBUTED_VERSION
from coiled.spans import span
from coiled.utils import error_info_for_tracking, unset_single_thread_defaults

from ..v2.widgets.rich import LightRichClusterWidget
from .cluster.better_logs import better_logs
from .utils import CONTEXT_SETTINGS

MINIMUM_DISTRIBUTED_VERSION = Version("2023.6.0")


class KeepaliveSession:
    def __init__(self, cluster, prefix=""):
        self.cluster = cluster
        rand_uuid = coiled.utils.short_random_string()
        self.session_id = f"{prefix}-{rand_uuid}" if prefix else rand_uuid

    def __enter__(self):
        # keepalive session lets us use keepalive without dask client
        self.cluster._call_scheduler_comm("coiled_add_keepalive_session", name=self.session_id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cluster._call_scheduler_comm("coiled_end_keepalive_session", name=self.session_id)


def get_ssh_connection(cloud, cluster_id):
    try:
        import fabric
        from paramiko.ed25519key import Ed25519Key
    except ImportError:
        # shouldn't get here but just in case
        raise RuntimeError("--use-ssh requires fabric")

    ssh_info = cloud.get_ssh_key(cluster_id=cluster_id)

    with io.StringIO(ssh_info["private_key"]) as f:
        pkey = Ed25519Key(file_obj=f)

    connection = fabric.connection.Connection(
        ssh_info["scheduler_public_address"], user="ubuntu", connect_kwargs={"pkey": pkey}
    )

    return connection


def run_via_ssh(cloud, cluster, info, command, file, interactive):
    try:
        import invoke
    except ImportError:
        # shouldn't get here but just in case
        raise RuntimeError("--use-ssh requires fabric")

    connection = get_ssh_connection(cloud, cluster.cluster_id)
    results = None

    original_command = " ".join(command)
    callstack = [{"code": original_command, "relative_line": 0}]
    # Extract and upload files from `command`
    command = shlex.split(original_command)
    info["files-implicit"] = []
    for idx, i in enumerate(command):
        if os.path.exists(i) and os.path.isfile(i):
            # flatten paths, everything will be /scratch/foo
            # without any subdirectories
            connection.put(i, "/scratch/")
            info["files-implicit"].append(i)
            # adjust command to reference path on VM
            command[idx] = f"/scratch/{os.path.basename(i)}"

            # include code files in the "callstack"
            if i.endswith((".py", ".sh")):
                try:
                    with open(i) as f:
                        contents = f.read()
                    callstack.append({"code": contents, "filename": i})
                except Exception:
                    pass

    # Upload user-specified files too
    info["files-explicit"] = file
    for f in file:
        connection.put(f, "/scratch/")

    command_string = " ".join(command)

    container_name = "tmp-dask-1"

    entrypoint = get_entrypoint(connection, container_name)
    if "cloud-env" in entrypoint:
        # hack for cloud-env containers (e.g., package sync) currently required to avoid re-downloading senv
        # once container is suitably changed, we should just be able to use entrypoint like any other container
        entrypoint = "micromamba run -p /opt/coiled/env"

    docker_opts = "-it" if interactive else ""

    container_command = f"docker exec --workdir /scratch {docker_opts} {container_name} {entrypoint} {command_string}"
    try:
        with KeepaliveSession(cluster=cluster, prefix="ssh"), span(cluster, callstack=callstack):
            results = connection.run(container_command, hide=not interactive, pty=interactive)
    except invoke.exceptions.UnexpectedExit as e:
        results = str(e)
    except Exception as e:
        raise e

    return connection, container_command, results


def get_entrypoint(connection, container_name) -> str:
    entrypoint = ""
    x = connection.run(f"docker inspect -f '{{{{json .Config.Entrypoint}}}}' {container_name}", hide=True)
    if x.stdout:
        entrypoint = json.loads(x.stdout)

        if entrypoint:
            # hack so we don't use `tini` for each run, remove everything between `tini` and `--`
            # e.g., "tini -g -- /usr/bin/prepare.sh" -> "/usr/bin/prepare.sh"
            if "tini" in entrypoint[0]:
                if "--" in entrypoint:
                    after_tini = entrypoint.index("--")
                    entrypoint = entrypoint[after_tini + 1 :]

            entrypoint = " ".join(entrypoint) if entrypoint else ""
    return entrypoint or ""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--name",
    default=None,
    help="Run name. If not given, defaults to a unique name.",
)
@click.option(
    "--account",
    default=None,
    help="Coiled account (uses default account if not specified)",
)
@click.option(
    "--software",
    default=None,
    help=(
        "Software environment name to use. If neither software nor container is specified, "
        "all the currently-installed Python packages are replicated on the VM using package sync."
    ),
)
@click.option(
    "--container",
    default=None,
    help=(
        "Container image to use. If neither software nor container is specified, "
        "all the currently-installed Python packages are replicated on the VM using package sync."
    ),
)
@click.option(
    "--vm-type",
    default=[],
    multiple=True,
    help="VM type to use. Specify multiple times to provide multiple options.",
)
@click.option(
    "--gpu",
    default=False,
    is_flag=True,
    help="Have a GPU available.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the notebook.",
)
@click.option(
    "--disk-size",
    default=None,
    help="Use larger-than-default disk on VM, specified in GiB.",
)
@click.option(
    "--keepalive",
    default=None,
    help=(
        "Keep your VM running for the specified time, even after your command completes. "
        "In seconds (`--keepalive 60`) unless you specify units (`--keepalive 3m` for 3 minutes)."
        "Default to shutdown immediately after the command finishes."
    ),
)
@click.option(
    "--file",
    "-f",
    default=[],
    multiple=True,
    help="Local files required to run command.",
)
@click.option(
    "--use-ssh",
    default=False,
    is_flag=True,
    hidden=True,
)
@click.option(
    "--interactive",
    default=False,
    is_flag=True,
    hidden=True,
)
@click.argument("command", nargs=-1)
def run(
    name: str,
    account: Optional[str],
    software: Optional[str],
    container: Optional[str],
    vm_type: Sequence[str],
    gpu: bool,
    region: Optional[str],
    disk_size: Optional[int],
    keepalive,
    file,
    use_ssh: bool,
    interactive: bool,
    command,
):
    """
    Run a command on the cloud.
    """
    if DISTRIBUTED_VERSION < MINIMUM_DISTRIBUTED_VERSION:
        # Relies on scheduler having scratch space, which was added in https://github.com/dask/distributed/pull/7802
        raise RuntimeError(
            f"`coiled run` requires distributed>={MINIMUM_DISTRIBUTED_VERSION} "
            f"(distributed={DISTRIBUTED_VERSION} is installed)"
        )

    if use_ssh:
        # while --use-ssh is hidden option we won't add fabric to client deps
        try:
            import fabric  # noqa: F401
        except ImportError:
            print(
                "[red][bold]Error:[/bold][/red] to use [green]--use-ssh[/green] "
                "you need to install [green]fabric[/green]"
            )
            return

    env = unset_single_thread_defaults()
    if container and "rapidsai" in container:
        env = {"DISABLE_JUPYTER": "true", **env}  # needed for "stable" RAPIDS image

    if not command:
        raise ValueError("command must be specified")

    keepalive = parse_timedelta(keepalive)
    shutdown_on_close = keepalive is None

    info = {"command": command, "keepalive": keepalive}
    success = True
    exception = None

    # if user tries `coiled run foo.py` they probably want to run `python foo.py` rather than `foo.py`
    if len(command) == 1 and command[0].endswith(".py"):
        command = ("python", command[0])

    connection = None
    container_command = None
    results = None

    try:
        with LightRichClusterWidget(
            account=account, title=f"Running [bold]{shlex.join(command)}[/bold]"
        ) as widget, coiled.Cloud(account=account) as cloud:
            account = account or cloud.default_account
            widget.update(
                server=cloud.server,
                cluster_details=None,
                logs=None,
                account=account,
            )
            info["account"] = account
            cluster_kwargs = dict(
                account=account,
                n_workers=0,
                software=software,
                container=container,
                scheduler_options={"idle_timeout": "24 hours"},
                scheduler_vm_types=list(vm_type) if vm_type else None,
                worker_vm_types=list(vm_type) if vm_type else None,
                allow_ssh=True,
                extra_worker_on_scheduler=True,
                environ=env,
                scheduler_gpu=gpu,
                region=region,
                shutdown_on_close=shutdown_on_close,
                tags={"coiled-cluster-type": "run/cli"},
                scheduler_disk_size=disk_size,
                worker_disk_size=disk_size,
            )
            token = tokenize(sys.executable, **cluster_kwargs)
            name = name or f"run-{token[:8]}"

            dask.config.set({"coiled.use_aws_creds_endpoint": True})
            with coiled.Cluster(name=name, cloud=cloud, custom_widget=widget, **cluster_kwargs) as cluster:
                info["cluster_id"] = cluster.cluster_id
                if not use_ssh:
                    with Client(cluster) as client:
                        if not shutdown_on_close:
                            cluster.set_keepalive(keepalive=keepalive)

                        original_command = " ".join(command)
                        callstack = [{"code": original_command, "relative_line": 0}]
                        # Extract and upload files from `command`
                        command = shlex.split(original_command)
                        info["files-implicit"] = []
                        for idx, i in enumerate(command):
                            if os.path.exists(i) and os.path.isfile(i):
                                client.upload_file(i, load=False)
                                info["files-implicit"].append(i)
                                command[idx] = os.path.basename(i)

                                # include code files in the "callstack"
                                if i.endswith((".py", ".sh")):
                                    try:
                                        with open(i) as f:
                                            contents = f.read()
                                        callstack.append({"code": contents, "filename": i})
                                    except Exception:
                                        pass

                        # Upload user-specified files too
                        info["files-explicit"] = file
                        for f in file:
                            client.upload_file(f, load=False)

                        def run_command(command):
                            subprocess.run(command, cwd=get_worker().local_directory)

                        info["command-parsed"] = command

                        # keep track of time before we start executing user code
                        start_ns = time.time_ns()

                        # TODO execute command in non-blocking way so we can also tail logs while it runs
                        client.submit(run_command, command=["echo", "@start-coiled-run"]).result()
                        with span(cluster, callstack=callstack):
                            client.submit(run_command, command=command).result()
                        client.submit(run_command, command=["echo", "@stop-coiled-run"]).result()
                else:
                    if not shutdown_on_close:
                        cluster.set_keepalive(keepalive=keepalive)

                    if interactive:
                        widget.stop()

                    start_ns = time.time_ns()
                    connection, container_command, results = run_via_ssh(
                        cloud, cluster, info, command, file, interactive
                    )

        if cluster.cluster_id and not interactive:
            print()

            print("Output")
            print("-" * len("Output"))
            print()

            if not use_ssh:
                better_logs(
                    cluster_id=cluster.cluster_id,
                    instance_labels_dict={},
                    show_label=False,
                    show_all_instances=True,
                    show_timestamp=False,  # only show the messages
                    tail=True,  # use tail so that we keep polling logs until stop sentinel to shows up
                    tail_max_times=10,  # only try 10 times (at 3s interval), logs should be ingested by then
                    since=str(int(start_ns // 1e6)),  # it wants timestamp in ms as a string
                    start_sentinel="@start-coiled-run",
                    stop_sentinel="@stop-coiled-run",
                )
            else:
                if results:
                    if isinstance(results, str):
                        print(results)
                    else:
                        print(results.stdout)
                        if results.stderr:
                            print(f"[red]{results.stderr}")

            print()

    except Exception as e:
        success = False
        exception = e
        raise e
    finally:
        coiled.add_interaction(
            "coiled-run-cli",
            success=success,
            **info,
            **error_info_for_tracking(exception),
        )
