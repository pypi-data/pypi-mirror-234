import os
import re
import shutil
import subprocess
import tempfile
from typing import Optional

import click
from rich import print
from rich.prompt import Confirm

import coiled

from ..utils import CONTEXT_SETTINGS
from .utils import find_cluster

DEFAULT_SSH_AGENT_CONFIG = "Host *.dask.host\n  IdentityAgent SSH_AUTH_SOCK"


def open_ssh(address: str, key: str, jump_to_address: Optional[str] = None, host_command: Optional[str] = None):
    """Open an SSH session, relies on `ssh` and `ssh-add` (agent)."""
    if not add_key_to_agent(address, key, t=5):
        return

    ssh_shell(address, jump_to_address, host_command)


def check_ssh() -> bool:
    if not shutil.which("ssh"):
        print("Unable to find `ssh`, you may need to install OpenSSH or add it to your paths.")
        return False

    if not shutil.which("ssh-add"):
        print("Unable to find `ssh-add`, you may need to install OpenSSH or add it to your paths.")
        return False

    return True


def check_ssh_agent():
    user_config_path = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_path):
        with open(user_config_path) as f:
            user_config = f.read()
            if "dask.host" in user_config:
                return True
            if re.search("IdentityAgent[^\n]+1password", user_config):
                print("Coiled cannot add temporary SSH key to [bold]1Password SSH Agent[/bold].")
                print(
                    "You can explicitly allow Coiled to use the system SSH agent by adding these lines to the "
                    f"beginning of [green]{user_config_path}[/green]:\n\n{DEFAULT_SSH_AGENT_CONFIG}\n\n"
                )
                if Confirm.ask("May Coiled edit your ssh config to add these lines?", default=True):
                    with open(user_config_path, "w") as f:
                        f.write(f"{DEFAULT_SSH_AGENT_CONFIG}\n\n{user_config}")
                    return True
                return False
    return True


def add_key_to_agent(address: str, key: str, t: Optional[int] = None, delete: bool = False) -> bool:
    """Add (or remove) ssh key to ssh agent."""
    if not check_ssh():
        return False

    with tempfile.TemporaryDirectory() as keydir:
        key_path = os.path.join(keydir, f"scheduler-key-{address}.pem")

        with open(key_path, "w") as f:
            f.write(key)

        # ssh needs file permissions to be set
        os.chmod(key_path, mode=0o600)

        cmd = ["ssh-add"]
        if delete:
            cmd.append("-d")
        if t:
            cmd.extend(["-t", f"{t}"])
        cmd.append(key_path)

        # briefly add key to agent, this allows us to jump to worker with agent forwarding
        p = subprocess.run(cmd, capture_output=True)

        if p.returncode and p.stderr:
            print("An error occurred calling `ssh-add`. You may need to enable the ssh agent.")
            print(p.stderr)
            return False

    return True


def ssh_shell(address: str, jump_to_address: Optional[str] = None, host_command: Optional[str] = None):
    if jump_to_address:
        ssh_target = f"-J ubuntu@{address} ubuntu@{jump_to_address}"
        ssh_target_label = f"worker at {jump_to_address}"
    else:
        ssh_target = f"ubuntu@{address}"
        ssh_target_label = f"scheduler at {address}"

    ssh_command = f"ssh -t {ssh_target} -o StrictHostKeyChecking=no -o ForwardAgent=yes"
    ssh_command = f"{ssh_command} {host_command}" if host_command else ssh_command

    print(f"===Starting SSH session to {ssh_target_label}===")
    if host_command:
        print(f"> {host_command}")
    subprocess.run(ssh_command, shell=True)
    print("===SSH session closed===")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--account",
    default=None,
    help="Coiled account (uses default account if not specified)",
)
@click.option(
    "--private",
    default=False,
    is_flag=True,
    help="Use private IP address of scheduler (default is public IP address)",
)
@click.option(
    "--worker",
    default=None,
    help="Connect to worker with specified name or private IP address (default is to connect to scheduler)",
)
@click.option(
    "--add-key",
    default=False,
    is_flag=True,
    help="Just add ssh key to local OpenSSH agent, no lifetime/expiration set",
)
@click.option(
    "--delete-key",
    default=False,
    is_flag=True,
    help="Just delete ssh key from local OpenSSH agent",
)
@click.option(
    "--dask", default=False, is_flag=True, help="Attach to shell in Dask container rather than shell on host machine."
)
@click.option(
    "--command",
    default=None,
    hidden=True,
)
def ssh(
    cluster: str,
    account: Optional[str],
    private: bool,
    worker: Optional[str],
    add_key: bool,
    delete_key: bool,
    dask: bool,
    command: Optional[str],
):
    with coiled.Cloud(account=account) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]
        ssh_info = cloud.get_ssh_key(cluster_id=cluster_id, worker=worker)

    scheduler_address = (
        ssh_info["scheduler_private_address"]
        if private
        else (ssh_info["scheduler_hostname"] or ssh_info["scheduler_public_address"])
    )

    if add_key:
        # just add the key, maybe you want to use rsync or something like that
        add_key_to_agent(scheduler_address, key=ssh_info["private_key"])

    elif delete_key:
        # just delete the key
        add_key_to_agent(scheduler_address, key=ssh_info["private_key"], delete=True)

    else:
        if not check_ssh_agent():
            print("You may get an error, but we'll try SSH anyway...")

        # open an ssh shell
        if ssh_info["scheduler_state"] not in ("starting", "started"):
            print(
                f"[red]Scheduler for {cluster_info['name']} ({cluster_id}) is "
                f"[bold]{ssh_info['scheduler_state']}[/bold]. "
                "You can only connect when scheduler is 'starting' or 'started'."
            )
            return

        if not scheduler_address:
            print(
                f"[red]Scheduler for {cluster_info['name']} ({cluster_id}) is "
                f"[bold]{ssh_info['scheduler_state']}[/bold] and does not currently have an IP address.[/]"
            )
            return

        if not ssh_info["private_key"]:
            print("Unable to retrieve SSH key")
            return

        # Default container name is parent dir (tmp) + service name (dask) + instance number (1).
        # If we need to make this more flexible in the future, name could be returned by cloud.get_ssh_key;
        # for now we don't need that flexibility and it's okay if SSH CLI requires client update someday.
        command = f"docker exec -it tmp-dask-1 {command or 'bash'}" if dask else command

        open_ssh(
            address=scheduler_address,
            key=ssh_info["private_key"],
            jump_to_address=ssh_info["worker_address"],
            host_command=command,
        )
