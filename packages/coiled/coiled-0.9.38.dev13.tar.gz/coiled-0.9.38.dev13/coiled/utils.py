from __future__ import annotations

import asyncio
import contextlib
import functools
import itertools
import json
import logging
import numbers
import os
import platform
import random
import re
import ssl
import string
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import uuid
import warnings
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from hashlib import md5
from logging.config import dictConfig
from math import ceil
from pathlib import Path
from typing import Dict, Iterable, List, NoReturn, Optional, Set, Tuple, Union
from urllib.parse import unquote, urlencode, urlparse
from zipfile import PyZipFile

import backoff
from packaging.version import Version

from coiled.context import get_datadog_trace_link, track_context

if sys.version_info >= (3, 8):
    from typing import Literal, Type, TypedDict
else:
    from typing_extensions import Literal, Type, TypedDict

import aiohttp
import boto3
import click
import dask.config
import dask.utils
import rich
import urllib3
import yaml
from dask.distributed import Security
from rich.console import Console

from coiled.exceptions import (
    AccountFormatError,
    ApiResponseStatusError,
    AuthenticationError,
    CidrInvalidError,
    GPUTypeError,
    InstanceTypeError,
    ParseIdentifierError,
    PortValidationError,
    UnsupportedBackendError,
)
from coiled.types import AWSOptions, FirewallOptions, GCPOptions

from .compatibility import COILED_VERSION, PY_VERSION
from .errors import ServerError

logger = logging.getLogger(__name__)

COILED_DIR = str(Path(__file__).parent)
ACCOUNT_REGEX = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)*$")
ALLOWED_PROVIDERS = ["aws", "vm_aws", "gcp", "vm_gcp"]

COILED_LOGGER_NAME = "coiled"
COILED_SERVER = "https://cloud.coiled.io"
COILED_RUNTIME_REGEX = re.compile(r"^coiled/coiled-runtime-(?P<version>\d+\-\d+\-\d+)-*")

# Dots after family names ensure we do not match t3a or other variants
AWS_BALANCED_INSTANCES_FAMILY_FILTER = ("t2.", "t3.", "m5.", "m6i.", "t4g.", "m6g.", "m7g.")
AWS_INSTANCES_FAMILY_FILTER = AWS_BALANCED_INSTANCES_FAMILY_FILTER  # deprecated
AWS_GPU_INSTANCE_FAMILIES_FILTER = ("g4dn",)
AWS_UNBALANCED_INSTANCE_FAMILIES_FILTER = ("c5.", "c6i.", "r6i.", "c7g.", "r7g.")

GCP_SCHEDULER_GPU = {
    "scheduler_accelerator_type": "nvidia-tesla-t4",
    "scheduler_accelerator_count": 1,
}

# Directories to ignore when building wheels from source
IGNORE_PYTHON_DIRS = {"build", "dist", "docs", "tests"}

COILED_LOCAL_PACKAGE_PREFIX = "coiled_local_"


class VmType(TypedDict):
    """
    Example:
        {
        'name': 't2d-standard-8',
        'cores': 8,
        'gpus': 0,
        'gpu_name': None,
        'memory': 32768,
        'backend_type': 'vm_gcp'
        }
    """

    name: str
    cores: int
    gpus: int
    gpu_name: str
    memory: int
    backend_type: str
    coiled_credits: float


# TODO: copied from distributed, introduced in 2021.12.0.
# We should be able to remove this someday once we can increase
# the minimum supported version.
def in_async_call(loop, default=False):
    """Whether this call is currently within an async call"""
    try:
        return loop.asyncio_loop is asyncio.get_running_loop()
    except RuntimeError:
        # No *running* loop in thread. If the event loop isn't running, it
        # _could_ be started later in this thread though. Return the default.
        if not loop.asyncio_loop.is_running():
            return default
        return False


def validate_account(account: str):
    if ACCOUNT_REGEX.match(account) is None:
        raise AccountFormatError(
            f"Bad account format. Account '{account}' should be a combination "
            "of lowercase letters, numbers and hyphens."
        )


def random_str(length: int = 8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


class GatewaySecurity(Security):
    """A security implementation that temporarily stores credentials on disk.

    The normal ``Security`` class assumes credentials already exist on disk,
    but our credentials exist only in memory. Since Python's SSLContext doesn't
    support directly loading credentials from memory, we write them temporarily
    to disk when creating the context, then delete them immediately."""

    def __init__(self, tls_key, tls_cert, extra_conn_args: Optional[dict] = None):
        self.tls_scheduler_key = tls_key
        self.tls_scheduler_cert = tls_cert
        self.extra_conn_args = extra_conn_args or {}

    def __repr__(self):
        return "GatewaySecurity<...>"

    def get_connection_args(self, role):
        ctx = None
        if self.tls_scheduler_key and self.tls_scheduler_cert:
            with tempfile.TemporaryDirectory() as tempdir:
                key_path = os.path.join(tempdir, "dask.pem")
                cert_path = os.path.join(tempdir, "dask.crt")
                with open(key_path, "w") as f:
                    f.write(self.tls_scheduler_key)
                with open(cert_path, "w") as f:
                    f.write(self.tls_scheduler_cert)
                ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=cert_path)
                ctx.verify_mode = ssl.CERT_REQUIRED
                ctx.check_hostname = False
                ctx.load_cert_chain(cert_path, key_path)
        return {
            "ssl_context": ctx,
            "require_encryption": True,
            "extra_conn_args": self.extra_conn_args,
        }


async def handle_api_exception(response, exception_cls: Type[Exception] = ServerError) -> NoReturn:
    with contextlib.suppress(aiohttp.ContentTypeError, json.JSONDecodeError, AttributeError):
        # First see if it's an error we created that has a more useful
        # message
        error_body = await response.json()
        if isinstance(error_body, dict):
            errs = error_body.get("non_field_errors")
            if "message" in error_body:
                raise exception_cls(error_body["message"])
            elif errs and isinstance(errs, list) and len(errs):
                raise exception_cls(errs[0])
            else:
                raise exception_cls("Server error, ".join(f"{k}={v}" for (k, v) in error_body.items()))
        else:
            raise exception_cls(error_body)

    error_text = await response.text()

    if not error_text:
        # Response contains no text/body, let's not raise an empty exception
        error_text = f"{response.status} - {response.reason}"
    raise exception_cls(error_text)


def normalize_server(server: Optional[str]) -> str:
    if not server:
        server = COILED_SERVER
    # Check if using an older server
    if "beta.coiledhq.com" in server or "beta.coiled.io" in server:
        # NOTE: https is needed here as http is not redirecting
        server = COILED_SERVER

    # remove any trailing slashes
    server = server.rstrip("/")

    return server


def get_account_membership(user_dict: dict, memberships: list, account: Optional["str"] = None) -> Optional[dict]:
    if account is None:
        account = user_dict.get("default_account")
        account = account.get("slug") if account else None

    for membership in memberships:
        account_details = membership.get("account", {})
        has_membership = account_details.get("slug") == account
        if has_membership:
            return membership

    else:
        return None


def get_auth_header_value(token: str) -> str:
    """..."""
    # TODO: delete the branching after client only supports ApiToken.
    if "-" in token:
        return "ApiToken " + token
    else:
        return "Token " + token


def has_program_quota(account_usage: dict) -> bool:
    return account_usage.get("has_quota") is True


async def login_if_required(
    *,
    server: Optional[str] = None,
    token: Optional[str] = None,
    account: Optional[str] = None,
    save: Optional[bool] = None,
    use_config: bool = True,
    retry: bool = True,
    browser: Optional[bool] = None,
):
    account = account or dask.config.get("coiled.account", None)
    # "save" bool means always/never, None means try to do the thing that makes sense
    if save is None:
        # if token is already set in config and isn't being changed, then no need to save again
        if dask.config.get("coiled.token", None) and (not token or token == dask.config.get("coiled.token")):
            save = False
        else:
            # user doesn't already have token saved, so save it without asking
            save = True

    if use_config:
        token = token or dask.config.get("coiled.token")
        server = server or dask.config.get("coiled.server")
        if "://" not in server:
            server = "http://" + server
        server = server.rstrip("/")
        account = account or dask.config.get("coiled.account")

    try:
        await handle_credentials(server=server, token=token, account=account, save=save, retry=retry, browser=browser)
    except ImportError as e:
        rich.print(f"[red]{e}")


@backoff.on_exception(backoff.expo, ApiResponseStatusError, logger=logger)
async def _fetch_data(*, session, server, endpoint):
    response = await session.request("GET", f"{server}{endpoint}")
    if response.status == 426:
        # client version upgrade required
        await handle_api_exception(response)
    elif response.status in [401, 403]:
        raise AuthenticationError(f"Auth Error: {response.status}. Invalid Token")
    elif response.status in [502, 503, 504]:
        raise ApiResponseStatusError(
            f"Unable to receive data from the server. Received {response.status} - Temporary Error."
        )
    elif response.status >= 400:
        await handle_api_exception(response)
    return await response.json()


# We only use ApiResponseStatusError on status 502, 503, 504
async def handle_credentials(
    *,
    server: Optional[str] = None,
    token: Optional[str] = None,
    account: Optional[str] = None,
    save: Optional[bool] = None,
    retry: bool = True,
    print_invalid_token_messages: bool = True,
    browser: Optional[bool] = None,
) -> Tuple[str, str, str, list]:
    """Validate and optionally save credentials

    Parameters
    ----------
    server
        Server to connect to. If not specified, will check the
        ``coiled.server`` configuration value.
    token
        Coiled user token to use. If not specified, will prompt user
        to input token.
    account
        Name of Coiled account to use. If not provided, will
        default to the user's default account.
    save
        Whether or not save credentials to coiled config file.
        If ``None``, will ask for input on whether or not credentials
        should be saved. Defaults to None.
    retry
        Whether or not to try again if invalid credentials are entered.
        Retrying is often desired in interactive situations, but not
        in more programmatic scenerios. Defaults to True.

    Returns
    -------
    user
        Username
    token
        User API token
    server
        Server being used
    memberships
        List of account memberships
    """

    is_account_specified = bool(account)
    if account:
        validate_account(account)

    # If testing locally with `ngrok` we need to
    # rewrite the server to localhost
    server = server or dask.config.get("coiled.server", COILED_SERVER)
    server = normalize_server(server)

    browser = True if browser is None else browser

    if token is None:
        from .auth import client_token_grant_flow

        result = await client_token_grant_flow(server, browser, account=account)
        if result:
            return result
        raise ValueError(
            "Authorization failed. Please try to login again, and if the error persists, "
            "please reach out to Coiled Support at support@coiled.io"
        )

    # TODO: revert when we remove versioneer
    if dask.config.get("coiled.no-minimum-version-check", False):
        client_version = "coiled-frontend-js"
    else:
        client_version = COILED_VERSION
    account_usage = {}
    # Validate token and get username
    async with aiohttp.ClientSession(
        headers={
            "Authorization": get_auth_header_value(token),
            "Client-Version": client_version,
        }
    ) as session:
        try:
            user_dict = await _fetch_data(
                session=session,
                server=server,
                endpoint="/api/v2/user/me",
            )
        except AuthenticationError:
            if print_invalid_token_messages:
                rich.print("[red]Invalid Coiled token encountered[/red]")
            if retry:
                return await handle_credentials(server=server, token=None, account=account, save=None, retry=False)
            else:
                if print_invalid_token_messages:
                    rich.print(
                        "You can use [green]coiled login[/green] to authorize a new token for your Coiled client, "
                        "or contact us at support@coiled.io if you continue to have problems."
                    )
                raise
        memberships = await _fetch_data(session=session, server=server, endpoint="/api/v2/user/me/memberships")
        if not isinstance(memberships, list) or not memberships:
            account_membership = None
            memberships = []
        else:
            account_membership = get_account_membership(user_dict, memberships, account=account)
        # only validate if account arg is provided by user
        if account and not account_membership:
            rich.print("[red]You are not a member of this account. Perhaps try another one?\n")
            account = click.prompt("Account")
            if account:
                validate_account(account)
            else:
                rich.print("[red]No account provided, unable to login.")

            return await handle_credentials(server=server, token=token, save=None, account=account)

        if account_membership and not account:
            account = account_membership.get("account", {}).get("slug")

        # We should always have username from above, but let's be defensive about it just in case.
        user = user_dict.get("username")
        if not user:
            raise ValueError(
                "Unable to get your account username after login. Please try to login again, if "
                "the error persists, please reach out to Coiled Support at support@coiled.io"
            )

        # Avoid extra printing when creating clusters
        if save is not False:
            rich.print("[green]Authentication successful[/green] 🎉")
            # Only get account usage when we are actually going to check it
            account_usage = await _fetch_data(
                session=session, server=server, endpoint=f"/api/v2/user/account/{account}/usage"
            )
            if not isinstance(account_usage, dict):
                account_usage = {}
            if not has_program_quota(account_usage):
                rich.print("[red]You have reached your quota of Coiled credits for this account.")
    if save is None:
        # Optionally save user credentials for next time
        save_creds = input("Save credentials for next time? [Y/n]: ")
        if save_creds.lower() in ("y", "yes", ""):
            save = True
    if save:
        creds = {
            "coiled": {
                "user": user,
                "token": token,
                "server": server,
            }
        }
        if is_account_specified and account:
            # If user didn't specify account, don't set it in the local config file because
            # when it's set, it overrides default account set on server.
            creds["coiled"]["account"] = account

        config, config_file = save_config(new_config=creds)
        rich.print(f"Credentials have been saved at {config_file}")
        # Make sure saved configuration values are set for the current Python process.
        dask.config.update(dask.config.config, config)

    return user, token, server, memberships


def save_config(new_config: dict) -> tuple[dict, str]:
    """Save new config values to Coiled config file, return new config and path to file."""
    config_file = os.path.join(os.path.expanduser("~"), ".config", "dask", "coiled.yaml")
    # Make sure directory with config exists
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    configs = dask.config.collect_yaml([config_file])

    config = dask.config.merge(*configs, new_config)
    with open(config_file, "w") as f:
        f.write(yaml.dump(config))
    return config, config_file


class Spinner:
    """A spinner context manager to denotate we are still working"""

    def __init__(self, delay=0.2):
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.busy = False

    def write_next(self):
        with self._screen_lock:
            sys.stdout.write(next(self.spinner))
            sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            sys.stdout.write("\b")
            if cleanup:
                sys.stdout.write(" ")  # overwrite spinner with blank
                sys.stdout.write("\r")  # move to next line
            sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write("\r")


def parse_identifier(
    identifier: str,
    property_name: str = "name",
    can_have_revision: bool = False,
    allow_uppercase: bool = False,
) -> Tuple[Optional[str], str, Optional[str]]:
    """
    Parameters
    ----------
    identifier:
        identifier of the resource, i.e. "coiled/xgboost" "coiled/xgboost:1ef489", "xgboost:1ef489" or "xgboost"
    can_have_revision:
        Indicates if this identifier supports having a ":<string>" postfix, as in
        the ":1ef489" in "xgboost:1ef489". At time of writing, this only has an effect
        on software environments. For other resources this has no meaning. At time
        of writing, this only affects the error message that will be printed out.
    property_name:
        The name of the parameter that was being validated; will be printed
        with any error messages, i.e. Unsupported value for "software_environment".

    Examples
    --------
    >>> parse_identifier("coiled/xgboost", "software_environment")
    ("coiled", "xgboost", None)
    >>> parse_identifier("xgboost", "software_environment", False)
    (None, "xgboost", None)
    >>> parse_identifier("coiled/xgboost:1ef4543", "software_environment", True)
    ("coiled", "xgboost", "1ef4543")

    Raises
    ------
    ParseIdentifierError
    """
    if allow_uppercase:
        rule = re.compile(r"^([a-zA-Z0-9-_]+?/)?([a-zA-Z0-9-_]+?)(:[a-zA-Z0-9-_]+)?$")
        rule_text = ""
    else:
        rule = re.compile(r"^([a-z0-9-_]+?/)?([a-z0-9-_]+?)(:[a-zA-Z0-9-_]+)?$")
        rule_text = "lowercase "

    match = re.fullmatch(rule, identifier)
    if match:
        account, name, revision = match.groups()
        account = account.replace("/", "") if account else account
        revision = revision.replace(":", "") if revision else revision
        return account, name, revision

    if can_have_revision:
        message = (
            f"'{identifier}' is invalid {property_name}: should have format (<account>/)<name>(:<revision>),"
            ' for example "coiled/xgboost:1efd456", "xgboost:1efd456" or "xgboost". '
            f"It can only contain {rule_text}ASCII letters, numbers, hyphens and underscores. "
            "The <name> is required (xgboost in the previous example). The <account> prefix"
            f" can be used to specify a {property_name} from a different account, and the"
            f" :<revision> can be used to select a specific revision of the {property_name}."
        )
    else:
        message = (
            f"'{identifier}' is invalid {property_name}: should have format (<account>/)<name>,"
            f' for example "coiled/xgboost" or "python-37". and can only contain {rule_text}ASCII letters,'
            ' numbers, hyphens and underscores. The <name> is required ("xgboost" and "python-37"'
            " in the previous examples)."
            f' The <account> prefix (i.e. "coiled/") can be used to specify a {property_name}'
            " from a different account."
        )
    raise ParseIdentifierError(message)


def get_platform():
    # Determine platform
    if sys.platform == "linux":
        platform = "linux"
    elif sys.platform == "darwin":
        platform = "osx"
    elif sys.platform == "win32":
        platform = "windows"
    else:
        raise ValueError(f"Invalid platform {sys.platform} encountered")
    return platform


class ExperimentalFeatureWarning(RuntimeWarning):
    """Warning raise by an experimental feature"""

    pass


class DeprecatedFeatureWarning(RuntimeWarning):
    pass


def experimental(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is an experimental feature which is subject "
            "to breaking changes, being removed, or otherwise updated without notice "
            "and should be used accordingly.",
            ExperimentalFeatureWarning,
        )
        return func(*args, **kwargs)

    return inner


async def run_command_in_subprocess(cmd: str, suppress_error: bool = False):
    """Run the command in subprocess.

    If a user is using a python version < 3.8 then he will get a RuntimeError exception -
    ``Cannot add child handler, the child watcher does not have a loop attached``. As a
    workaround for the issue, we check if the user is running any earlier version of python
    and run the command in subprocess instead.

    For reference on the RuntimeError exception: https://bugs.python.org/issue35621

    """
    platform = get_platform()

    if PY_VERSION < Version("3.8") or platform == "windows":
        proc = subprocess.Popen(
            cmd.split(" "),
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert proc.stdout
        for line in proc.stdout:
            yield line.rstrip()

    else:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        lines = []
        while proc.stdout and proc.stderr and proc.returncode is None:
            await asyncio.sleep(0.5)
            async for line in proc.stdout:
                line = line.decode(encoding=sys.stdout.encoding or "utf-8").rstrip()
                lines.append(line)
                yield line

            async for line in proc.stderr:
                line = line.decode(encoding=sys.stderr.encoding or "utf-8").rstrip()
                lines.append(line)
                yield line

        if proc.returncode and not suppress_error:
            raise ValueError("\n".join(lines))


def name_exists_in_dict(user: Union[str, None], name: Union[str, None], dictionary: Union[dict, None]) -> bool:
    """Check if name exists in dictionary.

    Since we are returning ``<account>/<name>`` when listing software envs
    and cluster configs, this method will try to handle the case where sometimes
    we are passing a name with the format ``<account>/<name>`` and sometimes with
    ``<name``.

    If we can't find ``<account>/<name>`` in the dictionary, we will check if we
    can find the ``name`` substring in the dictionary keys.

    """
    if dictionary:
        if f"{user}/{name}" in dictionary or name in dictionary:
            return True
        if any([soft_env for soft_env in dictionary if name in soft_env]):
            return True
    return False


def rich_console():
    is_spyder = False

    with contextlib.suppress(AttributeError, ImportError):
        from IPython.core.getipython import get_ipython

        ipython = get_ipython()
        if ipython and ipython.config.get("SpyderKernelApp"):
            is_spyder = True

    if is_spyder:
        print("Creating Cluster. This usually takes 1-2 minutes...")
        return Console(force_jupyter=False)
    return Console()


@backoff.on_exception(backoff.expo, Exception, max_time=10)
def verify_aws_credentials_with_retry(aws_access_key_id: str, aws_secret_access_key: str):
    verify_aws_credentials(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def verify_aws_credentials(aws_access_key_id: str, aws_secret_access_key: str):
    """Verify AWS Credentials are valid, raise exception so caller knows what is wrong with credentials."""
    sts = boto3.client(
        "sts",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    sts.get_caller_identity()


def scheduler_ports(protocol: Union[str, List[str]]):
    """Generate scheduler ports based on protocol(s)"""
    exclude = 8787  # dashboard port
    start = 8786
    if isinstance(protocol, str):
        return start

    port = start
    ports = []
    for _ in protocol:
        if port == exclude:
            port += 1
        ports.append(port)
        port += 1
    return ports


def parse_gcp_region_zone(region: Optional[str] = None, zone: Optional[str] = None):
    """Parse GCP zone and region or return default region/zone.

    This is an helper function to make it easier for us
    to parse gcp zones. Since users can specify regions,
    zones or one of the two, we should create some sane
    way to deal with the different combinations.

    """
    if not region and not zone:
        region = "us-east1"
        zone = "us-east1-c"
    elif region and zone and len(zone) == 1:
        zone = f"{region}-{zone}"
    elif not region and zone and len(zone) == 1:
        region = "us-east1"
        zone = f"{region}-{zone}"
    elif zone and not region:
        region = zone[:-2]

    return region, zone


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


def enable_debug_mode():
    from .context import COILED_SESSION_ID

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "utc": {
                "()": UTCFormatter,
                "format": "[UTC][%(asctime)s][%(levelname)-8s][%(name)s] %(message)s",
            },
        },
        "handlers": {
            "utc-console": {
                "class": "logging.StreamHandler",
                "formatter": "utc",
            },
        },
        "loggers": {
            "coiled": {
                "handlers": ["utc-console"],
                "level": logging.DEBUG,
            },
        },
    }
    dictConfig(LOGGING)
    logger.debug(f"Coiled Version : {COILED_VERSION}")
    start = datetime.now(tz=timezone.utc)
    trace_link = get_datadog_trace_link(start=start, **{"coiled-session-id": COILED_SESSION_ID})
    logger.info(f"DD Trace: {trace_link}")
    trace_link = get_datadog_logs_link(start=datetime.now(tz=timezone.utc), **{"coiled-session-id": COILED_SESSION_ID})
    logger.info(f"DD Logs: {trace_link}")


def get_datadog_logs_link(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    **filters: Dict[str, str],
):
    params = {
        "query": " ".join([f"@{k}:{v}" for k, v in filters.items()]),
        "live": "false",
    }
    if start:
        fuzzed = start - timedelta(minutes=1)
        params["from_ts"] = str(int(fuzzed.timestamp() * 1000))
    if end:
        fuzzed = end + timedelta(minutes=1)
        params["to_ts"] = str(int(fuzzed.timestamp() * 1000))
    return f"https://app.datadoghq.com/logs?{urlencode(params)}"


def validate_gpu_type(gpu_type: str):
    """Validate gpu type provided by the user.

    Currently, we are just accepting the nvidia-tesla-t4 gpu type
    but in the next iteration we will accept more types. We are also
    filtering out virtual workstation gpus upstream, so we need this
    function to remove types that we know it will fail.

    """

    if gpu_type != "nvidia-tesla-t4":
        error_msg = f"GPU type '{gpu_type}' is not a supported GPU type. Allowed " "GPU types are: 'nvidia-tesla-t4'."
        raise GPUTypeError(error_msg)
    return True


def is_gcp(account: str, accounts: dict) -> bool:
    """Determine if an account backend is Google Cloud Provider.

    Parameters
    ----------
    account: str
        Slug of Coiled account to use.
    accounts: dict
        Dictionary of available accounts from the /api/v1/users/me endpoint.

    Returns
    -------
    gcp_backend: bool
        True if a GCP backend, else False.
    """
    user_account = accounts.get(account, {})
    user_options = user_account.get("options", {})
    gcp_backend = user_account.get("backend") == "vm_gcp" or user_options.get("provider_name") == "gcp"
    return gcp_backend


def is_customer_hosted(account: str, accounts: dict) -> bool:
    """Determine if an account backend is customer-hosted.

    Parameters
    ----------
    account: str
        Slug of Coiled account to use.
    accounts: dict
        Dictionary of available accounts from the /api/v1/users/me endpoint.

    Returns
    -------
    customer_hosted: bool
        True if a customer-hosted backend, else False.
    """
    user_account = accounts.get(account, {})
    backend_type = user_account.get("backend")
    customer_hosted = backend_type == "vm"
    return customer_hosted


def validate_cidr_block(cidr_block: str):
    """Validate cidr block added by the user.

    Here we are only checking if the cidr block is in the
    format <int>.<int>.<int>.<int>/<int>.

    """
    if not isinstance(cidr_block, str):
        raise CidrInvalidError(
            f"CIDR needs to be of type string, but received '{type(cidr_block)}' "
            "please specify your CIDR block as a string."
        )
    match = re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}\/\d{1,3}", cidr_block)
    if not match:
        raise CidrInvalidError(
            f"The CIDR block provided '{cidr_block}' doesn't appear "
            "to have the correct IPV4 pattern, your CIDR block should "
            "follow the '0.0.0.0/0' pattern."
        )
    return True


def validate_ports(ports):
    """Validate the ports tha the user tries to pass.

    We need to make sure that the user passes a list of ints only,
    otherwise we should raise an exception.

    """
    if not isinstance(ports, list):
        raise PortValidationError(
            f"Ports need to be of type list, but received '{type(ports)}' " "please adds your ports in a list."
        )

    for port in ports:
        if not isinstance(port, int):
            raise PortValidationError(
                f"Ports need to be of type int, but received '{type(port)}' "
                "please use a int value for your port number."
            )
    return True


def validate_network(backend_options: dict, is_customer_hosted: bool):
    """Validate network configuration from backend options.

    Users can specify network and/or subnet(s) to use. We need to validate these and
    ensure that they're only used with customer hosted backend.
    """
    if not is_customer_hosted:
        raise UnsupportedBackendError(
            "Network configuration isn't available in a Coiled "
            "hosted backend. Please change your backend to configure network."
        )

    network_options = backend_options.get("network", {})

    # check that resource ids, if specified, are strings
    resource_ids = (
        network_options.get("network_id"),
        network_options.get("scheduler_subnet_id"),
        network_options.get("worker_subnet_id"),
        network_options.get("firewall_id"),
    )

    for resource_id in resource_ids:
        if resource_id and not isinstance(resource_id, str):
            raise TypeError(f"Network id '{id}' for '{resource_id}' must be a string.")


def parse_backend_options(
    backend_options: dict,
    account: str,
    accounts: dict,
    worker_gpu: Optional[int],
) -> dict:
    """Parse backend options before launching cluster.

    The following are checked and parsed before launching a cluster:
        - If launching into a GCP cluster, `preemptible` is aliased with `spot`.
        - If requesting worker GPUs, `spot` defaults to `False` unless specified.
        - If set, `zone` overrides `gcp_zone` (for GCP).

    Parameters
    ----------
    backend_options: dict
        Dictionary of backend specific options (e.g. ``{'region': 'us-east-2'}``).
    account: str
        Slug of Coiled account to use.
    accounts: dict
        Dictionary of available accounts from the /api/v1/users/me endpoint.
    worker_gpu: int
        Number of GPUs allocated for each worker.

    Returns
    -------
    backend_options: dict
        A dictionary of parsed backend options.
    """
    backend_options = deepcopy(backend_options)
    gcp_backend = is_gcp(account, accounts)
    customer_hosted = is_customer_hosted(account, accounts)
    # alias preemptible/spot
    if backend_options.get("preemptible") is not None and gcp_backend:
        backend_options["spot"] = backend_options.pop("preemptible")
    # default to on-demand for gpu workers
    if backend_options.get("spot") is None and bool(worker_gpu):
        backend_options["spot"] = False

    # zone (if set) overrides gcp_zone for gcp
    if backend_options.get("zone") and backend_options.get("gcp_project_name"):
        backend_options["gcp_zone"] = backend_options.get("zone")

    if backend_options.get("network"):
        validate_network(backend_options, customer_hosted)
    if backend_options.get("firewall"):
        cidr = backend_options["firewall"].get("cidr")
        ports = backend_options["firewall"].get("ports")
        if ports:
            validate_ports(ports)
        if cidr:
            validate_cidr_block(cidr)
    return backend_options


async def get_worker_creation_notification_error(cloud, account: Optional[str]) -> Optional[str]:
    """Call get_notifications and return error messages from worker creation.

    When we try to create workers, we use the ``create_worker`` event type to
    the notification, we can quickly use this event type and the logging level
    ``ERROR`` to only get notifications that are related to worker creation.

    Note that we don't use the cluster name in the backend, but the cluster id
    so we can't really filter the notifications by name, with that in mind, we
    make the assumption that the last notification that we receive will be the
    one from the cluster that just ran. This is ugly but should work okay for
    now.

    """
    notifications = await cloud.get_notifications(account=account, json=True, event_type="create_worker", level="ERROR")

    if notifications:
        last_notification = notifications[-1]
        error_message = last_notification.get("data", {}).get("error")

        # If there is no reason, lets avoiding showing "giving up" messages
        # with no useful message
        if error_message and "Reason" in error_message:
            return error_message
        return last_notification["msg"]


def parse_wait_for_workers(n_workers: int, wait_for_workers: Optional[bool | int | float] = None) -> int:
    """Parse the option to wait for workers."""
    wait_for_workers = (
        # Set 30% as default value to wait for workers
        dask.config.get("coiled.wait-for-workers", 0.3) if wait_for_workers is None else wait_for_workers
    )

    if wait_for_workers is True:
        to_wait = n_workers
    elif wait_for_workers is False:
        to_wait = 0
    elif isinstance(wait_for_workers, int):
        if wait_for_workers >= 0 and wait_for_workers <= n_workers:
            to_wait = wait_for_workers
        else:
            raise ValueError(
                f"Received invalid value '{wait_for_workers}' as wait_for_workers, "
                f"this value needs to be between 0 and {n_workers}"
            )
    elif isinstance(wait_for_workers, float):
        if wait_for_workers >= 0 and wait_for_workers <= 1.0:
            to_wait = ceil(wait_for_workers * n_workers)
        else:
            raise ValueError(
                f"Received invalid value '{wait_for_workers}' as wait_for_workers, "
                "this value needs to be a value between 0 and 1.0."
            )
    else:
        raise ValueError(
            f"Received invalid value '{wait_for_workers}' as wait_for_workers, "
            "this value needs to be either a Boolean, an Integer or a Float."
        )

    return to_wait


def bytes_to_mb(bytes: float) -> int:
    """Convert bytes to Mb.

    Our backend expects the memory to be passed as Mb, so we need to convert
    bytes obtained by dask to Mb.

    """
    return round(abs(bytes) * 10**-6)


def parse_requested_memory(
    memory: Optional[Union[int, str, float, List[str], List[int], List[float]]],
    min_memory: Optional[Union[str, int, float]],
) -> dict:
    """Handle memory requested by user.

    Users calling `list_instance_types` can use different ways to specify memory,
    this function will handle the different cases and return a dictionary with the
    expected result.

    Note: We are also giving a +- 10% buffer on the requested memory.

    """
    parsed_memory = {}

    if isinstance(memory, list):
        if len(memory) > 2:
            raise ValueError(
                f"Memory should contain only two values in the format `[minimum, maximum]`, but received {memory}."
            )
        parsed_memory["memory__gte"] = bytes_to_mb(dask.utils.parse_bytes(memory[0]) * 0.89)
        parsed_memory["memory__lte"] = bytes_to_mb(dask.utils.parse_bytes(memory[1]) * 1.1)
    elif isinstance(memory, int) or isinstance(memory, float) or isinstance(memory, str):
        parsed_memory["memory__gte"] = bytes_to_mb(dask.utils.parse_bytes(memory) * 0.89)
        parsed_memory["memory__lte"] = bytes_to_mb(dask.utils.parse_bytes(memory) * 1.1)

    if min_memory and not memory:
        parsed_memory["memory__gte"] = bytes_to_mb(dask.utils.parse_bytes(min_memory))

    return parsed_memory


@track_context
def get_instance_type_from_cpu_memory(
    cpu: Optional[Union[int, List[int]]] = None,
    memory: Optional[Union[int, str, float, List[int], List[str], List[float]]] = None,
    gpus: Optional[int] = None,
    backend: Optional[str] = None,
    arch: Literal["x86_64", "arm64"] = "x86_64",
) -> List[str]:
    """Get instances by cpu/memory combination.

    We are using the `list_instance_types` method to get the
    instances that match the cpu/memory specification. If no
    instance can be found we will raise an exception
    informing the user about this.

    """
    # Circular imports
    from .core import list_instance_types

    if backend == "gcp":
        instance_family = "n1" if gpus else "e2"
        instances = [
            instance_name
            for instance_name in list_instance_types(cores=cpu, memory=memory, backend=backend, arch=arch)
            if instance_name.startswith(instance_family)
        ]
    else:
        instance_types = list_instance_types(cores=cpu, memory=memory, backend=backend, gpus=gpus, arch=arch)

        aws_family_filter = AWS_BALANCED_INSTANCES_FAMILY_FILTER
        if gpus:
            aws_family_filter = AWS_GPU_INSTANCE_FAMILIES_FILTER
        elif cpu and memory:
            aws_family_filter += AWS_UNBALANCED_INSTANCE_FAMILIES_FILTER

        instances = [instance_name for instance_name in instance_types if instance_name.startswith(aws_family_filter)]

    if not instances:
        error_message = (
            "\n"
            "Unable to find instance types that match the specification: \n"
            f"    Cores: {cpu}  Memory: {memory} GPUs: {gpus}  Arch: {arch}\n"
        )

        if (isinstance(memory, numbers.Number) and memory < 1e9) or (  # type: ignore
            isinstance(memory, (tuple, list)) and all(isinstance(m, numbers.Number) and m < 1e9 for m in memory)  # type: ignore
        ):
            error_message += f"""
Your specified memory, {memory}, was too low. Memory units are in bytes.
We recommend strings like "32 GiB", or numbers like 32e9.
"""

        if cpu or memory:
            error_message += (
                "\n"
                "You can select a range for the cpu or memory, for example:"
                "\n    `cpu=[2, 8]` or `memory=['32 GiB','64GiB'] \n"
            )

        if cpu and memory:
            memory_matching_instances = [
                instance_name for instance_name in list_instance_types(memory=memory, backend=backend)
            ]

            if memory_matching_instances:
                error_message += (
                    "You might want to pick these instances that match your "
                    "memory requirements, but have different core count. \n"
                    f"{memory_matching_instances} \n"
                )
        error_message += (
            "\n"
            "You can also use the following to list instance types:"
            f'\n    coiled.list_instance_types(backend="{backend}")\n'
            "\nand use the `scheduler_vm_types=[]` or `worker_vm_types=[]`"
            "\nkeyword arguments to specify your desired instance type."
        )
        raise InstanceTypeError(error_message)
    return instances


def any_gpu_instance_type(type_list: Optional[Union[str, List[str]]]) -> bool:
    # TODO (future PR) ideally we'd get this from database via endpoint as part of preflight check
    #   but for now we'll just use regex to match instance types with bundled GPU
    if not type_list:
        return False
    if isinstance(type_list, str):
        type_list = [type_list]
    # check supported AWS instance types and GCP type with non-guest GPU (A100)
    return any(
        re.search(r"^(((p4|p3|g5|g5g|g4dn|g4ad)\.)|(a2-))", vm_type, flags=re.IGNORECASE) for vm_type in type_list
    )


def validate_backend_options(backend_options):
    # both typing.TypedDict and typing_extensions.TypedDict have __optional_keys__
    aws_keys = set(AWSOptions.__optional_keys__)  # type: ignore
    gcp_keys = set(GCPOptions.__optional_keys__)  # type: ignore

    # show warning for unknown keys
    all_keys = set().union(aws_keys, gcp_keys)
    for key in backend_options.keys():
        if key in ("firewall_spec",):
            # firewall_spec isn't currently in user-schema, but it's how we send the data
            # to backend endpoint.
            # `{"ingress": [...]}` (user) —> `{firewall_spec: {"ingress": [...]}` (endpoint)
            continue
        if key not in all_keys:
            logger.warning(f"{key} in backend_options is not a recognized key, it will be ignored")
        if key in ("firewall", "send_prometheus_metrics", "prometheus_write"):
            logger.warning(f"{key} in backend_options is deprecated")

    # validate that we don't have aws and gcp-specific keys
    present_aws_keys = [key for key in backend_options.keys() if key in aws_keys - gcp_keys]
    present_gcp_keys = [key for key in backend_options.keys() if key in gcp_keys - aws_keys]
    if present_aws_keys and present_gcp_keys:
        raise ValueError(
            f"backend_options cannot have both AWS specific keys ({present_aws_keys}) "
            f"and GCP specific keys ({present_gcp_keys}"
        )

    # validate firewall options
    if backend_options.get("ingress"):
        if not isinstance(backend_options["ingress"], Iterable):
            raise ValueError("ingress in backend_options must be an iterable")

        firewall_keys = FirewallOptions.__optional_keys__  # type: ignore
        for fw in backend_options["ingress"]:
            for key in fw.keys():
                if key not in firewall_keys:
                    logger.warning(f"{key} ({fw[key]}) in backend_options firewall config is not a recognized key")

            for required_key in ("cidr", "ports"):
                if not fw.get(required_key):
                    raise ValueError(f"{required_key} is required for each firewall config")

            if not isinstance(fw["cidr"], str):
                raise ValueError(f"cidr ({fw['cidr']}) must be a string")
            if not isinstance(fw["ports"], list):
                raise ValueError(f"ports ({fw['ports']} must be a list")

    # validate optional bool, dict, int, str types
    all_key_types = {
        **AWSOptions.__annotations__,
        **GCPOptions.__annotations__,
    }
    keys_by_type = {
        t: [k for k, key_type in all_key_types.items() if key_type == Optional[t]] for t in (bool, dict, int, str)
    }
    for t, schema_keys in keys_by_type.items():
        for key in backend_options.keys():
            if key in schema_keys:
                val = backend_options[key]
                # all keys as optional, but if specified, they need to match desired type
                if val is not None and not isinstance(val, t):
                    raise ValueError(
                        f"{key} ({val}) in backend_options should be {t.__name__} or None, not {type(val).__name__}"
                    )


def validate_vm_typing(vm_types: Union[List[str], Tuple[str], None]):
    """Validate instance typing.

    We need to add this function because the error that our API is returning
    isn't exactly user friendly. We should raise a type error with an informative
    message instead of the dictionary that the API throws.

    """
    if not vm_types:
        return
    if not isinstance(vm_types, (list, tuple)):
        raise TypeError(
            f"Instance types must be a list or tuple, but the value '{vm_types}' is of "
            f"type: {type(vm_types)}. Please use a list of strings when specifying "
            "instance types."
        )
    for instance in vm_types:
        if not isinstance(instance, str):
            raise TypeError(
                f" Instance types must be a string, but '{instance}' is of type "
                f"{type(instance)}. Please use a string instead."
            )


def name_to_version(name: str) -> Version:
    matched = COILED_RUNTIME_REGEX.match(name)
    if matched is None:
        return Version("0.0.0")  # Should not happen
    return Version(matched.group("version").replace("-", "."))


def get_details_url(server, account, cluster_id):
    if cluster_id is None:
        return None
    else:
        return f"{server}/clusters/{cluster_id}?account={account}"


def get_grafana_url(
    cluster_details,
    account,
    cluster_id,
    grafana_server="grafana.dev-sandbox.coiledhq.com",
):
    cluster_name = cluster_details["name"]

    # for stopped clusters, only get metrics until the cluster stopped
    if cluster_details["current_state"]["state"] in ("stopped", "error"):
        end_ts = int(datetime.fromisoformat(cluster_details["current_state"]["updated"]).timestamp() * 1000)
    else:
        end_ts = "now"

    start_ts = int(datetime.fromisoformat(cluster_details["scheduler"]["created"]).timestamp() * 1000)

    base_url = f"https://{grafana_server}/d/eU1bT-nVz/cluster-metrics-prometheus?orgId=1"
    datasource = "default"  # FIXME
    # FIXME -- get account name for cluster

    full_url = (
        f"{base_url}"
        f"&datasource={datasource}"
        f"&var-env=All"
        f"&var-account={account}"
        f"&var-cluster={cluster_name}"
        f"&var-cluster-id={cluster_id}"
        f"&from={start_ts}"
        f"&to={end_ts}"
    )

    return full_url


def cluster_firewall(
    target: str,
    scheduler: int = 8786,
    dashboard: Optional[int] = 8787,
    jupyter: bool = False,
    ssh: bool = False,
    http: bool = False,
    https: bool = True,
):
    """
    Easier cluster firewall configuration when using a single CIDR.

    Examples
    --------
    To create a cluster than only accepts connections from your IP address,
    and opens port 22 for SSH access:
    >>> coiled.Cluster(
            ...,
            backend_options={**coiled.utils.cluster_firewall("me", ssh=True)}
        )

    Parameters
    ----------
    target: str
        Open cluster firewall to this range. You can either specify a CIDR,
        or use "me" to automatically get your IP address and use that, or
        "everyone" for "0.0.0.0/0".
    scheduler: int
        Port to open for access to scheduler, 8786 by default.
    dashboard: Optional[int]
        Port to open for access to dashboard, 8787 by default.
        Use `None` to not open a port for dashboard access.
    jupyter: bool
        Open port used for jupyter (8888), closed by default.
    ssh: bool
        Open port used for ssh (22), closed by default.
    http: bool
        Open port used for http (80), closed by default.
    https: bool
        Open port used for https (443), open by default.
    """
    if target == "everyone":
        cidr = "0.0.0.0/0"
    elif target == "me":
        # get public/internet routable address from which local user will be hitting scheduler
        with urllib3.PoolManager() as pool:
            my_public_ip = pool.request("GET", "https://api.ipify.org").data.decode("utf-8")

        cidr = f"{my_public_ip}/32"
    else:
        # TODO validate this this is cidr
        cidr = target

    ports = [scheduler]

    if dashboard:
        ports.append(dashboard)

    if ssh:
        ports.append(22)
    if jupyter:
        ports.append(8888)
    if http:
        ports.append(80)
    if https:
        ports.append(443)
    return {"ingress": [{"ports": ports, "cidr": cidr}]}


def is_legal_python_filename(filename: str):
    return filename.endswith(".py") and filename[:-3].isidentifier()


def recurse_importable_python_files(src: Path):
    skip_dirs = set()
    if platform.system() == "Darwin":
        skip_dirs = {
            (Path.home() / "Applications").resolve(),
            (Path.home() / "Desktop").resolve(),
            (Path.home() / "Documents").resolve(),
            (Path.home() / "Downloads").resolve(),
            (Path.home() / "Library").resolve(),
            (Path.home() / "Movies").resolve(),
            (Path.home() / "Music").resolve(),
            (Path.home() / "Pictures").resolve(),
            (Path.home() / "Public").resolve(),
        }
    dir_has_py = {}
    dot_path = Path(".")
    for root, dirs, files in os.walk(src, topdown=True):
        root_path = Path(root)
        rel_root = root_path.relative_to(src)
        has_py = False
        # Don't need .get because we always iterate through parents before
        # children, and the only case where there isn't a parent is when
        # rel_root == dot_path.
        parent_has_py = rel_root == dot_path or dir_has_py[rel_root.parent]

        for file in files:
            if is_legal_python_filename(file):
                has_py = True
                yield rel_root / file

        dir_has_py[rel_root] = has_py
        for d in dirs[:]:
            if (
                not d.isidentifier()
                or (root_path / d).resolve() in skip_dirs
                # Let's assume we can stop looking if there are no Python files
                # three levels deep.
                # For example, ./a/b/c/module.py would only be yielded if
                # there's a .py file in ./a/ or ./a/b/.
                or (not has_py and not parent_has_py and rel_root.parent != dot_path)
            ):
                # pruning inplace like this works as long as topdown=True
                dirs.remove(d)


async def validate_wheel(wheel: Path, src: str) -> Tuple[bool, str, Set[str]]:
    """
    Validate a wheel contains some python files and return the md5

    Also, warn if there are Python files in src directory that are not
    in the wheel.
    """
    hash = md5()
    has_python = False
    src_python_files = set()
    # Check if src is a URL and not a local path. This works for both Unix and
    # Windows because the drive letter in windows will get parsed as the scheme
    # and its length will be 1.
    if len(urlparse(src).scheme) > 1:
        src_path = Path(src)
        if (src_path / "src").exists():
            src_path = src_path / "src"
        for p in recurse_importable_python_files(src_path):
            parent_names = {parent.name for parent in p.parents}
            if not parent_names.intersection(IGNORE_PYTHON_DIRS):
                src_python_files.add(str(p))

    with PyZipFile(str(wheel), mode="r") as wheelzip:
        info = wheelzip.infolist()
        for file in info:
            src_python_files.discard(file.filename)

            if not has_python and file.filename != "__init__.py" and file.filename.endswith(".py"):
                has_python = True
            if "dist-info" not in file.filename:
                hash.update(str(file.CRC).encode())

    return has_python, hash.hexdigest(), src_python_files


def get_aws_identity():
    import boto3
    import botocore

    response = {}

    session = boto3.Session()
    sts = session.client("sts")

    def get_account_alias() -> str:
        try:
            iam = session.client("iam")
            r = iam.list_account_aliases()
            return r.get("AccountAliases", [])[0]
        except Exception:
            return ""

    try:
        identity = sts.get_caller_identity()

        response["account"] = identity.get("Account")
        response["who"] = identity.get("Arn").split(":")[-1]

        alias = get_account_alias()
        if alias:
            response["account_alias"] = alias
    except botocore.exceptions.NoCredentialsError:
        response["error"] = "NoCredentialsError"
    except Exception as e:
        response["error"] = str(e)

    return response


def parse_file_uri(file_uri: str) -> Path:
    p = urlparse(file_uri)
    unquoted_path = unquote(p.path)
    if os.name == "nt":
        # handling valid windows URIs of
        # file:///C:/somewhere/something.whl
        unquoted_path = unquoted_path.lstrip("/")
    return Path(unquoted_path)


def is_system_python() -> bool:
    """Determine if the current Python executable is a system Python."""
    # Check if we are in a virtualenv
    if (
        "VIRTUAL_ENV" in os.environ
        or "PYENV_VERSION" in os.environ
        or getattr(sys, "base_prefix", sys.prefix) != sys.prefix
        or getattr(sys, "real_prefix", sys.prefix) != sys.prefix
        or os.path.exists(os.path.join(sys.prefix, "conda-meta"))
    ):
        return False
    # Check installation directory for each OS
    system = platform.system()
    if system == "Linux" and sys.prefix == "/usr":
        return True
    if system == "Darwin" and (sys.prefix.startswith("/Library") or sys.prefix.startswith("/System")):
        return True
    # Default to False
    return False


NOT_INTERESTING_STACK_CODE = (
    "distributed/utils.py",
    "coiled/context.py",
    "tornado/gen.py",
    "backoff/_async.py",
    "aiohttp/client.py",
    "yarl/_url.py",
)

NOT_INTERESTING_FUNCTION = (
    "_depaginate",
    "_do_request",
    "_sync",
    "sync",
)


def is_interesting_stack_frame(filename, function):
    if any(f in filename for f in NOT_INTERESTING_STACK_CODE):
        return False
    if "coiled" in filename and (any(f in function for f in NOT_INTERESTING_FUNCTION) or function.endswith("_page")):
        return False
    return True


def truncate_traceback(exc_traceback):
    curr = exc_traceback
    frames = []
    shown = set()

    while curr:
        filename = curr.tb_frame.f_code.co_filename
        function = curr.tb_frame.f_code.co_name

        if len(frames) == 0:
            # always keep first frame
            frames.append(curr)
            shown.add((filename, function))
        elif function.startswith("_") and (filename, function[1:]) in shown:
            # ignore _foo if we've already included foo
            pass
        elif is_interesting_stack_frame(filename, function):
            frames.append(curr)
            shown.add((filename, function))

        curr = curr.tb_next

    curr = None
    for tb in reversed(frames):
        tb.tb_next = curr
        curr = tb

    return curr


def error_info_for_tracking(error: Optional[BaseException] = None) -> dict:
    loc = {}
    if error:
        if error.__traceback__:
            error_trace = "\n".join(
                [
                    line if COILED_DIR in line else "...non coiled code..."
                    for line in traceback.format_tb(error.__traceback__)
                ]
            )
        else:
            error_trace = None
        loc = {
            "error_class": error.__class__.__name__,
            "error_message": str(error),
            "error_filename": "",
            "error_line": "",
            "error_trace": error_trace,
        }
        try:
            if error.__traceback__:
                loc["error_filename"] = error.__traceback__.tb_next.tb_next.tb_frame.f_code.co_filename  # type: ignore
                loc["error_line"] = str(error.__traceback__.tb_next.tb_next.tb_frame.f_lineno)  # type: ignore
        except Exception:
            pass
    return loc


def unset_single_thread_defaults() -> dict:
    """
    Returns the env vars required to unset the default pre-spawn config that makes certain libraries
    run in single-thread mode.
    """
    env = {}
    # there are libraries that distributed by default sets to be single-threaded
    # we want to unset these default values since we're running single task on a (potentially) big machine
    for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        if dask.config.get(f"distributed.nanny.pre-spawn-environ.{key}", 1) == 1:
            env = {key: "", **env}
    return env


def short_random_string():
    return str(uuid.uuid4())[:8]
