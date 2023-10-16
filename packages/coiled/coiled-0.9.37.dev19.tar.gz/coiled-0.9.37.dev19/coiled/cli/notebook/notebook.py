from __future__ import annotations

import asyncio
import os
import shutil
import signal
import subprocess
import webbrowser
from typing import Optional, Sequence, Tuple

import click
import importlib_metadata
from packaging.version import Version
from rich import print
from rich.control import Control
from rich.prompt import Confirm
from rich.segment import ControlType
from urllib3.util import parse_url

import coiled
from coiled.cli.cluster.ssh import add_key_to_agent, check_ssh, check_ssh_agent
from coiled.compatibility import DISTRIBUTED_VERSION
from coiled.errors import DoesNotExist
from coiled.utils import error_info_for_tracking

from ...v2.widgets.rich import LightRichClusterWidget
from ..utils import CONTEXT_SETTINGS

# Path on VM to sync to.
# We use `/scratch` for now because it's already bind-mounted into docker.
SYNC_TARGET = "/scratch/synced"
MIN_DISTRIBUTED_VERSION = Version("2022.8.1")
MUTAGEN_NAME_FORMAT = "coiled-{cluster_id}"


class NotebookError(Exception):
    pass


def check_distributed_version() -> bool:
    if DISTRIBUTED_VERSION < MIN_DISTRIBUTED_VERSION:
        print(
            "[bold red]"
            f"distributed>{MIN_DISTRIBUTED_VERSION} is required to launch notebooks. "
            f"You have {DISTRIBUTED_VERSION}."
            "[/]"
        )
        return False
    return True


def check_jupyter() -> bool:
    try:
        importlib_metadata.distribution("jupyterlab")
    except ModuleNotFoundError:
        print("[bold red]Jupyterlab must be installed locally to launch notebooks.[/]")
        return False

    try:
        importlib_metadata.distribution("jupyter_server_proxy")
    except ModuleNotFoundError:
        print(
            "[bold red]jupyter-server-proxy is not installed, "
            "without this you won't be able to access Dask dashboard for local clusters created on notebook server.[/]"
        )

    return True


def check_mutagen() -> bool:
    if not shutil.which("mutagen"):
        print(
            "[bold red]"
            "mutagen must be installed to synchronize files with notebooks.[/]\n"
            "Install via homebrew (on macOS, Linux, or Windows) with:\n\n"
            "brew install mutagen-io/mutagen/mutagen@0.16\n\n"
            "Or, visit https://github.com/mutagen-io/mutagen/releases/latest to download "
            "a static, pre-compiled binary for your system, and place it anywhere on your $PATH."
        )
        return False
    return True


def check_ssh_keygen() -> bool:
    if not shutil.which("ssh-keygen"):
        print("[bold red]Unable to find `ssh-keygen`, you may need to install OpenSSH or add it to your paths.[/]")
        return False
    return True


def mutagen_session_exists(cluster_id: int) -> bool:
    sessions = (
        subprocess.run(
            [
                "mutagen",
                "sync",
                "list",
                "--label-selector",
                f"managed-by=coiled,cluster-id={cluster_id}",
                "--template",
                "{{range .}}{{.Name}}{{end}}",
            ],
            text=True,
            capture_output=True,
        )
        .stdout.strip()
        .splitlines()
    )

    if not sessions:
        return False
    if sessions == [MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)]:
        return True

    if len(sessions) == 1:
        raise RuntimeError(
            f"Unexpected mutagen session name {sessions[0]!r}. "
            f"Expected {MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)!r}."
        )

    raise RuntimeError(f"Multiple mutagen sessions found for cluster {cluster_id}: {sessions}")


def connect_mutagen_sync(cloud, cluster_id, console) -> Tuple[bool, str]:
    if mutagen_session_exists(cluster_id):
        console.print("[bold]File sync session already active; reusing it.[/]")
    else:
        console.print("[bold]Launching file synchronization...[/]")
        ssh_info = cloud.get_ssh_key(cluster_id)

        scheduler_address = ssh_info["scheduler_hostname"] or ssh_info["scheduler_public_address"]
        target = f"ubuntu@{scheduler_address}"

        add_key_to_agent(scheduler_address, key=ssh_info["private_key"])

        # Update known_hosts. We can't specify SSH options to mutagen so we can't pass
        # `-o StrictHostKeyChecking=no`. Could alternatively add an entry in `~/.ssh/config`,
        # but that feels more intrusive.
        # TODO get public key from Coiled
        subprocess.run(
            f"ssh-keyscan {scheduler_address} >> ~/.ssh/known_hosts",
            shell=True,
            check=True,
            capture_output=True,
        )

        # Start mutagen
        result = subprocess.run(
            [
                "mutagen",
                "sync",
                "create",
                "--name",
                MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id),
                "--label",
                "managed-by=coiled",
                "--label",
                f"cluster-id={cluster_id}",
                "--ignore-vcs",
                "--max-staging-file-size=1 GiB",
                ".",
                f"{target}:{SYNC_TARGET}",
            ],
            check=False,
            text=True,
            capture_output=True,
        )

        # TODO show output live by wrapping console.print as file object that we pass to subprocess.run (?)
        if result.stderr:
            console.print(f"[red]Error attempting to connect sync...[/red]\n\n{result.stderr}")
        elif result.stdout:
            console.print(result.stdout)

        if result.returncode != 0:
            # there was a problem starting mutagen sync, so no reason to link the sync directory
            # (and most likely ssh is the problem so this too would fail)
            return False, result.stderr

        # Within the docker container, symlink the sync directory (`/scratch/sync`)
        # into the working directory for Jupyter, so you can actually see the synced
        # files in the Jupyter browser. We use a symlink since the container doesn't
        # have capabilities to make a bind mount.
        # TODO if we don't like the symlink, Coiled could see what the workdir is for
        # the image before running, and bind-mount `/sync` on the host to `$workdir/sync`
        # in the container? Custom docker images make this tricky; we can't assume anything
        # about the directory layout or what the working directory will be.
        subprocess.run(
            [
                "ssh",
                target,
                f"docker exec tmp-dask-1 bash -c 'mkdir -p {SYNC_TARGET} && ln -s {SYNC_TARGET} .'",
            ],
            check=True,
            capture_output=True,
        )
    return True, ""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--name",
    default=None,
    help="Cluster name. If not given, defaults to a hash based on current working directory.",
)
@click.option(
    "--account",
    default=None,
    help="Coiled account (uses default account if not specified)",
)
@click.option(
    "--sync",
    default=False,
    is_flag=True,
    help="Sync the working directory with the filesystem on the notebook. Requires mutagen.",
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
    help="Use GPU notebook server.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the notebook.",
)
@click.option(
    "--open",
    default=True,
    is_flag=True,
    help="Whether to open the notebook in the default browser once it's launched",
)
@click.option(
    "--block/--no-block",
    default=True,
    is_flag=True,
    help="Whether to block while the notebook is running.",
)
def start_notebook(
    name: Optional[str],
    account: Optional[str],
    sync: bool,
    software: Optional[str],
    container: Optional[str],
    vm_type: Sequence[str],
    gpu: bool,
    region: Optional[str],
    open: bool,
    block: bool,
):
    """
    Launch or re-open a notebook session, with optional file syncing.

    If a notebook session with the same ``name`` already exists, it's not re-created.
    If file sync was initially not enabled, running ``coiled notebook start --sync``
    will begin file sync without re-launching the notebook.
    """
    info = {"vm_type": vm_type, "sync": sync, "block": block}
    success = True
    exception = None

    try:
        # when using package sync, check that local env has jupyter and recent distributed
        if not software and not container:
            if not check_distributed_version():
                raise NotebookError("distributed version check")
            if not check_jupyter():
                raise NotebookError("jupyter missing")

        if sync and not (check_mutagen() and check_ssh() and check_ssh_keygen()):
            return

        if sync and not check_ssh_agent():
            print("Sync may be unable to start but we'll try anyway...")
            info["problem"] = "check_ssh_agent failed"

        env = None
        if container and "rapidsai" in container:
            env = {"DISABLE_JUPYTER": "true"}  # needed for "stable" RAPIDS image

        name = name or f"notebook-{coiled.utils.short_random_string()}"
        with LightRichClusterWidget(
            account=account, title=f"Notebook [bold]{name}[/bold]...", jupyter_link="...", width=84
        ) as widget, coiled.Cloud(account=account) as cloud:
            account = account or cloud.default_account
            info["account"] = account
            widget.update(
                server=cloud.server,
                cluster_details=None,
                logs=None,
                account=account,
                jupyter_link="...",
            )
            cluster = coiled.Cluster(
                name=name,
                cloud=cloud,
                n_workers=0,
                software=software,
                container=container,
                jupyter=True,
                scheduler_options={"idle_timeout": "24 hours"},
                scheduler_vm_types=list(vm_type) if vm_type else None,
                worker_vm_types=list(vm_type) if vm_type else None,
                allow_ssh=True,
                environ=env,
                scheduler_gpu=gpu,
                region=region,
                tags={"coiled-cluster-type": "notebook"},
                custom_widget=widget,
            )
            info["cluster_id"] = cluster.cluster_id

            url = cluster.jupyter_link
            cluster_id = cluster.cluster_id
            assert cluster_id is not None

            # by default, jupyter on the scheduler gives us client to that very scheduler
            # clear ENV var so default `Client()` on notebook gives us a new local cluster
            cluster.unset_env_vars(["DASK_SCHEDULER_ADDRESS"])

            if sync:
                url = parse_url(url)._replace(path="/jupyter/lab/tree/synced").url

            widget.update(
                cluster_details=None,
                logs=None,
                jupyter_link=url,
            )

            if sync:
                connected, error_message = connect_mutagen_sync(cloud, cluster_id, widget.live.console)
                if not connected:
                    widget.stop()
                    print(
                        "[red]Unable to start sync, see error shown above for more details.[/red]\n"
                        "If sync is not required, you can start notebook without [green]--sync[/green]."
                    )

                    _stop_notebook(name=name, account=account, cluster_id=cluster_id)

                    # close the cluster object so we comms close cleanly (and don't print error)
                    cluster.close()
                    raise NotebookError(f"unable to start sync: {error_message}")

            if open:
                webbrowser.open(url, new=2)

            if block:
                widget.update(
                    cluster_details=None,
                    logs=None,
                    trailer="Use Control-C to stop this notebook server",
                )

                def signal_handler_noop(_, frame):
                    # Ignore the input signal
                    return

                async def update_widget():
                    while True:
                        cluster_details = await cloud._get_cluster_details(cluster_id=cluster_id, account=account)
                        widget.update(cluster_details, logs=None)
                        # don't make user hit control-c if the cluster been stopped another way
                        if cluster_details["scheduler"]["current_state"]["state"] in ("error", "stopped"):
                            return False
                        await asyncio.sleep(1.0)

                while True:
                    try:
                        if not cluster.sync(update_widget):
                            widget.stop()
                            break
                    except KeyboardInterrupt:
                        widget.stop()
                        try:
                            exit = Confirm.ask("Are you sure you want to stop this notebook server?", default=True)
                        except KeyboardInterrupt:
                            exit = True
                        if exit:
                            # Register noop handler since we're shutting down and
                            # want to make sure the notebook is shutdown even when
                            # hammering ctrl-C
                            signal.signal(signal.SIGINT, signal_handler_noop)
                            break
                        else:
                            # write over the prompt
                            print(Control.move(0, -1), Control((ControlType.ERASE_IN_LINE, 2)))
                            print("[green]Continuing with this notebook server... [/]")

                            # move cursor to bottom of widget so widget won't shift
                            print(Control.move(0, -2))
                            widget.start()

                _stop_notebook(name=name, account=account, cluster_id=cluster_id)

                # close the cluster object so we comms close cleanly (and don't print error)
                cluster.close()
            else:
                stop_command = "coiled notebook stop"
                if account:
                    stop_command = f"{stop_command} --account {account}"
                stop_command = f"{stop_command} {name}"

                print(f"To stop this notebook server: [green]{stop_command}[/]")
    except NotebookError as e:
        success = False
        exception = e
        # don't raise, we've already printed appropriate message about the issue
    except Exception as e:
        success = False
        exception = e
        raise e
    finally:
        coiled.add_interaction(
            "coiled-notebook",
            success=success,
            **info,
            **error_info_for_tracking(exception),
        )


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
@click.option(
    "--account",
    default=None,
    help="Coiled account (uses default account if not specified)",
)
def stop_notebook(name: str, account: Optional[str]):
    """
    Shut down a notebook session
    """
    _stop_notebook(name=name, account=account)


def _stop_notebook(name: str, account: Optional[str], cluster_id: Optional[int] = None):
    with coiled.Cloud(account=account) as cloud:
        notebook_running = True
        try:
            cluster_id = cloud.get_cluster_by_name(name)
        except DoesNotExist:
            if cluster_id:
                print(f"[bold red]Notebook {name!r} is already stopped[/]")
            else:
                print(f"[bold red]Notebook {name!r} does not exist[/]")
            notebook_running = False

        if cluster_id and shutil.which("mutagen") and mutagen_session_exists(cluster_id):
            # NOTE: we can't tell if the user asked for `--sync` or not at creation.
            # Best we can do is check if mutagen is installed and the session exists.
            if not (check_ssh() and check_ssh_keygen()):
                return

            # Stop mutagen
            print(f"Stopping sync with notebook {name!r} ({cluster_id})")
            subprocess.run(["mutagen", "sync", "terminate", MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)])

            ssh_info = cloud.get_ssh_key(cluster_id)
            scheduler_address = ssh_info["scheduler_hostname"] or ssh_info["scheduler_public_address"]
            add_key_to_agent(scheduler_address, key=ssh_info["private_key"], delete=True)

            # Remove `known_hosts` entries.
            # TODO don't like touching the user's `known_hosts` file like this.
            subprocess.run(
                [
                    "ssh-keygen",
                    "-f",
                    os.path.expanduser("~/.ssh/known_hosts"),
                    "-R",
                    scheduler_address,
                ],
                capture_output=True,
            )

        if cluster_id and notebook_running:
            print(f"Stopping notebook {name!r} ({cluster_id})...")
            cloud.delete_cluster(cluster_id)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
def monitor_sync(name: str):
    "Monitor file sync status for a notebook session."
    if not check_mutagen():
        return

    with coiled.Cloud() as cloud:
        try:
            cluster_id = cloud.get_cluster_by_name(name)
        except DoesNotExist:
            print(f"[bold red]Cluster {name!r} does not exist[/]")
            return  # TODO exit 1

    if not mutagen_session_exists(cluster_id):
        print(f"[bold red]No file synchronization session for cluster {name!r} ({cluster_id})[/]")
        return  # TODO exit 1

    subprocess.run(["mutagen", "sync", "monitor", MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)])
