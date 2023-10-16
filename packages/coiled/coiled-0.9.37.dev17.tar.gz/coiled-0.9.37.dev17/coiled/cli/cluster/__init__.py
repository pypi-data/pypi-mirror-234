import click

from ..utils import CONTEXT_SETTINGS
from .better_logs import better_logs_cli as better_logs
from .logs import logs
from .ssh import ssh


@click.group(context_settings=CONTEXT_SETTINGS)
def cluster():
    """Commands for managing Coiled clusters"""
    pass


# @click.command(context_settings=CONTEXT_SETTINGS)
# def list():
#     print(f"...pretend this is a list of clusters...")


cluster.add_command(ssh)
cluster.add_command(logs, "logs-via-aws-cli")
cluster.add_command(better_logs, "logs")
cluster.add_command(better_logs)
