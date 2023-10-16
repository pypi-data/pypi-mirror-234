from __future__ import annotations

import asyncio
import contextlib
import datetime
import logging
import platform
import re
import time
import uuid
import warnings
import weakref
from asyncio import wait_for
from contextlib import suppress
from copy import deepcopy
from itertools import chain, islice
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Set,
    TypeVar,
    Union,
    cast,
    overload,
)

import botocore.exceptions
import dask.config
import dask.distributed
import dask.utils
from dateutil import tz
from distributed.core import Status
from distributed.deploy.adaptive import Adaptive
from distributed.deploy.cluster import Cluster as DistributedCluster
from packaging.version import Version
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from typing_extensions import Literal, TypeAlias
from urllib3.util import parse_url

from coiled.capture_environment import ResolvedPackageInfo, create_environment_approximation
from coiled.cluster import CoiledAdaptive, CredentialsPreferred
from coiled.compatibility import DISTRIBUTED_VERSION
from coiled.context import track_context
from coiled.core import IsAsynchronous
from coiled.errors import ClusterCreationError, DoesNotExist
from coiled.exceptions import ArgumentCombinationError, InstanceTypeError
from coiled.types import ArchitectureTypesEnum, AWSOptions, GCPOptions, PackageLevel, PackageLevelEnum
from coiled.utils import (
    COILED_LOGGER_NAME,
    GCP_SCHEDULER_GPU,
    any_gpu_instance_type,
    cluster_firewall,
    error_info_for_tracking,
    get_details_url,
    get_grafana_url,
    get_instance_type_from_cpu_memory,
    is_system_python,
    parse_identifier,
    parse_wait_for_workers,
    short_random_string,
    truncate_traceback,
    validate_vm_typing,
)

from ..core import Async, AWSSessionCredentials, Sync
from .core import (
    CloudV2,
    CloudV2SyncAsync,
    log_cluster_debug_info,
    setup_logging,
)
from .cwi_log_link import cloudwatch_url
from .states import (
    ClusterStateEnum,
    InstanceStateEnum,
    ProcessStateEnum,
    flatten_log_states,
    group_worker_errors,
    log_states,
    summarize_status,
)
from .widgets import EXECUTION_CONTEXT, ClusterWidget
from .widgets.rich import CONSOLE_WIDTH, RichClusterWidget, print_rich_package_table
from .widgets.util import simple_progress

logger = logging.getLogger(COILED_LOGGER_NAME)

_T = TypeVar("_T")


def use_rich_widget():
    return EXECUTION_CONTEXT in ["ipython_terminal", "notebook"]


TERMINATING_STATES = (
    Status.closing,
    Status.closed,
    Status.closing_gracefully,
    Status.failed,
)

BEHAVIOR_TO_LEVEL = {
    "critical-only": PackageLevelEnum.CRITICAL,
    "warning-or-higher": PackageLevelEnum.WARN,
    "any": PackageLevelEnum.NONE,
}
ClusterSyncAsync: TypeAlias = Union["Cluster[Async]", "Cluster[Sync]"]

_vm_type_cpu_memory_error_msg = (
    "Argument '{kind}_vm_types' can't be used together with '{kind}_cpu' or '{kind}_memory'. "
    "Please use either '{kind}_vm_types' or '{kind}_cpu'/'{kind}_memory' separately."
)


class Cluster(DistributedCluster, Generic[IsAsynchronous]):
    """Create a Dask cluster with Coiled

    Parameters
    ----------
    n_workers
        Number of workers in this cluster. Defaults to 4.
        If argument this is not specified, adaptive scaling is enabled.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    software
        Name of the software environment to use; this allows you to use and re-use existing
        Coiled software environments, and should not be used with package sync or when specifying
        a container to use for this specific cluster.
    container
        Name or URI of container image to use; when using a pre-made container image with Coiled,
        this allows you to skip the step of explicitly creating a Coiled software environment
        from that image. Note that this should not be used with package sync or when specifying
        an existing Coiled software environment.
    worker_class
        Worker class to use. Defaults to :class:`distributed.nanny.Nanny`.
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults
        to ``{}``.
    worker_vm_types
        List of instance types that you would like workers to use, default instance type
        selected contains 4 cores. You can use the command ``coiled.list_instance_types()``
        to see a list of allowed types.
    worker_cpu
        Number, or range, of CPUs requested for each worker. Specify a range by
        using a list of two elements, for example: ``worker_cpu=[2, 8]``.
    worker_memory
        Amount of memory to request for each worker, Coiled will use a +/- 10% buffer
        from the memory that you specify. You may specify a range of memory by using a
        list of two elements, for example: ``worker_memory=["2GiB", "4GiB"]``.
    worker_disk_size
        Non-default size of persistent disk attached to each worker instance, specified
        in GiB.
    worker_disk_throughput
        EXPERIMENTAL. For AWS, non-default throughput (in MB/s) for EBS gp3 volumes attached
        to workers.
    worker_gpu
        Number of GPUs to attach to each worker. Default is 0, ``True`` is interpreted as 1.
        Note that this is ignored if you're explicitly specifying an instance type which
        includes a fixed number of GPUs.
    worker_gpu_type
        For GCP, this lets you specify type of guest GPU for instances.
        Should match the way the cloud provider specifies the GPU, for example:
        ``worker_gpu_type="nvidia-tesla-t4"``.
        By default, Coiled will request NVIDIA T4 if GPU type isn't specified.
        For AWS, if you want GPU other than T4, you'll need to explicitly specify the VM
        instance type (e.g., ``p3.2xlarge`` for instance with one NVIDIA Tesla V100).
    scheduler_class
        Scheduler class to use. Defaults to :class:`distributed.scheduler.Scheduler`.
    scheduler_options
        Mapping with keyword arguments to pass to ``scheduler_class``. Defaults
        to ``{}``.
    scheduler_vm_types
        List of instance types that you would like the scheduler to use, default instances
        type selected contains 4 cores. You can use the command
        ``coiled.list_instance_types()`` to se a list of allowed types.
    scheduler_cpu
        Number, or range, of CPUs requested for the scheduler. Specify a range by
        using a list of two elements, for example: ``scheduler_cpu=[2, 8]``.
    scheduler_memory
        Amount of memory to request for the scheduler, Coiled will use a +/-10%
        buffer from the memory what you specify. You may specify a range of memory by using a
        list of two elements, for example: ``scheduler_memory=["2GiB", "4GiB"]``.
    scheduler_gpu
        Whether to attach GPU to scheduler; this would be a single NVIDIA T4.
        The best practice for Dask is to have a GPU on the scheduler if you are using GPUs on your
        workers, so if you don't explicitly specify, Coiled will follow this best practice and give
        you a scheduler GPU just in case you have ``worker_gpu`` set.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled. This object contains user/authentication/account
        information. If this is None (default), we look for a recently-cached Cloud object, and if none
        exists create one.
    account
        Name of Coiled account to use. If not provided, will
        default to the user account for the ``cloud`` object being used.
    shutdown_on_close
        Whether or not to shut down the cluster when it finishes.
        Defaults to True, unless name points to an existing cluster.
    idle_timeout
        Shut down the cluster after this duration if no activity has occurred. E.g. "30 minutes"
        Default: "20 minutes"
    use_scheduler_public_ip
        Boolean value that determines if the Python client connects to the
        Dask scheduler using the scheduler machine's public IP address. The
        default behaviour when set to True is to connect to the scheduler
        using its public IP address, which means traffic will be routed over
        the public internet. When set to False, traffic will be routed over
        the local network the scheduler lives in, so make sure the scheduler
        private IP address is routable from where this function call is made
        when setting this to False.
    use_dashboard_https
        When public IP address is used for dashboard, we'll enable HTTPS + auth by default.
        You may want to disable this if using something that needs to connect directly to
        the scheduler dashboard without authentication, such as jupyter dask-labextension<=6.1.0.
    credentials
        Which credentials to use for Dask operations and forward to Dask
        clusters -- options are "local", or None. The default
        behavior is to use local credentials if available.
        NOTE: credential handling currently only works with AWS credentials.
    credentials_duration_seconds
        For "local" credentials shipped to cluster as STS token, set the duration of STS token.
        If not specified, the AWS default will be used.
    timeout
        Timeout in seconds to wait for a cluster to start, will use
        ``default_cluster_timeout`` set on parent Cloud by default.
    environ
        Dictionary of environment variables. Values will be transmitted to Coiled; for private environment variables
        (e.g., passwords or access keys you use for data access), :meth:`send_private_envs` is recommended.
    send_dask_config
        Whether to send a frozen copy of local dask.config to the cluster.
    backend_options
        Dictionary of backend specific options.
    show_widget
        Whether to use the rich-based widget display in IPython/Jupyter (ignored if not in those environments).
        For use cases involving multiple Clusters at once, show_widget=False is recommended.
        (Default: True)
    custom_widget
        Use the rich-based widget display outside of IPython/Jupyter
        (Default: False)
    tags
        Dictionary of tags.
    wait_for_workers
        Whether to wait for a number of workers before returning control
        of the prompt back to the user. Usually, computations will run better
        if you wait for most workers before submitting tasks to the cluster.
        You can wait for all workers by passing ``True``, or not wait for any
        by passing ``False``. You can pass a fraction of the total number of
        workers requested as a float(like 0.6), or a fixed number of workers
        as an int (like 13). If None, the value from ``coiled.wait-for-workers``
        in your Dask config will be used. Default: 0.3. If the requested number
        of workers don't launch within 10 minutes, the cluster will be shut
        down, then a TimeoutError is raised.
    package_sync
        Synchronize package versions between your local environment and the cluster.
        Cannot be used with the ``software`` option. Passing ``True`` will sync all packages (recommended).
        If ``software`` is not given, defaults to True.
        Passing specific packages as a list of strings will attempt to synchronize only those packages,
        use with caution.
        We recommend reading the
        `additional documentation for this feature <https://docs.coiled.io/user_guide/package_sync.html>`_
    package_sync_ignore
        A list of package names to exclude from the environment. Note their dependencies may still be installed,
        or they may be installed by another package that depends on them!
    package_sync_strict
        Only allow exact packages matches, not recommended unless your client platform/architecture
        matches the cluster platform/architecture
    private_to_creator
        Only allow the cluster creator, not other members of team account, to connect to this cluster.
    use_best_zone
        Allow the cloud provider to pick the zone (in your specified region) that has best availability
        for your requested instances. We'll keep the scheduler and workers all in a single zone in
        order to avoid any interzone network traffic (which would be billed).
    spot_policy
        Purchase option to use for workers in your cluster, options are "on-demand", "spot", and
        "spot_with_fallback"; by default this is "on-demand".
        (Google Cloud refers to this as "provisioning model" for your instances.)
        **Spot instances** are much cheaper, but can have more limited availability and may be terminated
        while you're still using them if the cloud provider needs more capacity for other customers.
        **On-demand instances** have the best availability and are almost never
        terminated while still in use, but they're significantly more expensive than spot instances.
        For most workloads, "spot_with_fallback" is likely to be a good choice: Coiled will try to get as
        many spot instances as we can, and if we get less than you requested, we'll try to get the remaining
        instances as on-demand.
        For AWS, when we're notified that an active spot instance is going to be terminated,
        we'll attempt to get a replacement instance (spot if available, but could be on-demand if you've
        enabled "fallback"). Dask on the active instance will attempt a graceful shutdown before the
        instance is terminated so that computed results won't be lost.
    scheduler_port
        Specify a port other than the default (8786) for communication with Dask scheduler; this is useful
        if your client is on a network that blocks 8786.
    allow_ingress_from
        Control the CIDR from which cluster firewall allows ingress to scheduler; by default this is open
        to any source address (0.0.0.0/0). You can specify CIDR, or "me" for just your IP address.
    allow_ssh
        Allow connections to scheduler over port 22, used for SSH.
    jupyter
        Start a Jupyter server in the same process as Dask scheduler. The Jupyter server will be behind HTTPS
        with authentication (unless you disable ``use_dashboard_https``, which we strongly recommend against).
        Note that ``jupyterlab`` will need to be installed in the software environment used on the cluster
        (or in your local environment if using package sync).
        Once the cluster is running, you can use ``jupyter_link`` to get link to access the Jupyter server.
    region
        The cloud provider region in which to run the cluster.
    arm
        Use ARM instances for cluster; default is x86 (Intel) instances.
    """

    _instances = weakref.WeakSet()

    def __init__(
        self: ClusterSyncAsync,
        name: Optional[str] = None,
        *,
        software: Optional[str] = None,
        container: Optional[str] = None,
        n_workers: Optional[int] = None,
        worker_class: Optional[str] = None,
        worker_options: Optional[dict] = None,
        worker_vm_types: Optional[list] = None,
        worker_cpu: Optional[Union[int, List[int]]] = None,
        worker_memory: Optional[Union[str, List[str]]] = None,
        worker_disk_size: Optional[int] = None,
        worker_disk_throughput: Optional[int] = None,
        worker_gpu: Optional[Union[int, bool]] = None,
        worker_gpu_type: Optional[str] = None,
        scheduler_class: Optional[str] = None,
        scheduler_options: Optional[dict] = None,
        scheduler_vm_types: Optional[list] = None,
        scheduler_cpu: Optional[Union[int, List[int]]] = None,
        scheduler_memory: Optional[Union[str, List[str]]] = None,
        scheduler_disk_size: Optional[int] = None,
        scheduler_gpu: Optional[bool] = None,
        asynchronous: bool = False,
        cloud: Optional[CloudV2] = None,
        account: Optional[str] = None,
        shutdown_on_close=None,
        idle_timeout: Optional[str] = None,
        use_scheduler_public_ip: Optional[bool] = None,
        use_dashboard_https: Optional[bool] = None,
        credentials: Optional[str] = "local",
        credentials_duration_seconds: Optional[int] = None,
        timeout: Optional[Union[int, float]] = None,
        environ: Optional[Dict[str, str]] = None,
        tags: Optional[Dict[str, str]] = None,
        send_dask_config: bool = True,
        backend_options: Optional[Union[AWSOptions, GCPOptions]] = None,  # intentionally not in the docstring yet
        show_widget: bool = True,
        custom_widget: Optional[ClusterWidget] = None,
        configure_logging: Optional[bool] = None,
        wait_for_workers: Optional[Union[int, float, bool]] = None,
        package_sync: Union[bool, List[str]] = False,
        package_sync_strict: bool = False,
        package_sync_ignore: Optional[List[str]] = None,
        package_sync_fail_on: Literal["critical-only", "warning-or-higher", "any"] = "critical-only",
        private_to_creator: Optional[bool] = None,
        use_best_zone: bool = True,
        # "compute_purchase_option" is the old name for "spot_policy"
        # someday we should deprecate and then remove compute_purchase_option
        compute_purchase_option: Optional[Literal["on-demand", "spot", "spot_with_fallback"]] = None,
        spot_policy: Optional[Literal["on-demand", "spot", "spot_with_fallback"]] = None,
        extra_worker_on_scheduler: Optional[bool] = None,
        _n_worker_specs_per_host: Optional[int] = None,
        # easier network config
        scheduler_port: Optional[int] = None,
        allow_ingress_from: Optional[str] = None,
        allow_ssh: Optional[bool] = None,
        jupyter: Optional[bool] = None,
        region: Optional[str] = None,
        arm: Optional[bool] = None,
    ):
        if n_workers is None:
            # local variable instead of instance attribute would work fine,
            # except that I want to send this to mix panel, and self._as_json_compatible
            # wants to look at instance attributes
            self.start_adaptive = True
            n_workers = 4
        else:
            self.start_adaptive = False

        # NOTE:
        # this attribute is only updated while we wait for cluster to come up
        self.errored_worker_count: int = 0
        self.init_time = datetime.datetime.now()
        type(self)._instances.add(self)

        senv_kwargs = {"package_sync": package_sync, "software": software, "container": container}
        set_senv_kwargs = [name for name, value in senv_kwargs.items() if value]
        if len(set_senv_kwargs) > 1:
            raise ValueError(
                f"Multiple software environment parameters are set: {', '.join(set_senv_kwargs)}. "
                "You must use only one of these."
            )
        self.package_sync = bool(package_sync)  # TODO: this should be mutually exclusive with passing a software env
        self.package_sync_ignore = package_sync_ignore
        if isinstance(package_sync, list):
            # ensure python is always included
            self.package_sync_only = set(package_sync)
            self.package_sync_only.add("python")
        else:
            self.package_sync_only = None
        self.package_sync_strict = package_sync_strict
        self.package_sync_fail_on = BEHAVIOR_TO_LEVEL[package_sync_fail_on]
        self.show_widget = show_widget
        self.custom_widget = custom_widget
        self.arch = ArchitectureTypesEnum.ARM64 if arm else ArchitectureTypesEnum.X86_64

        self._cluster_status_logs = []

        if region is not None:
            if backend_options is None:
                backend_options = {}
            # backend_options supports both `region` and `region_name` (for backwards compatibility
            # since we changed it at some point).
            # If either of those is specified along with kwarg `region=`, raise an exception.
            if "region_name" in backend_options:
                raise ValueError(
                    "You passed `region` as a kwarg to Cluster(...), and included region_name"
                    " in the backend_options dict. Only one of those should be specified."
                )
            if "region" in backend_options:
                raise ValueError(
                    "You passed `region` as a kwarg to Cluster(...), and included region"
                    " in the backend_options dict. Only one of those should be specified."
                )
            backend_options["region_name"] = region

        if configure_logging:
            setup_logging()

        if configure_logging is None:
            # setup logging only if we're not using the widget
            if not (custom_widget or use_rich_widget()):
                setup_logging()

        # Determine consistent sync/async
        if cloud and asynchronous is not None and cloud.asynchronous != asynchronous:
            warnings.warn(
                f"Requested a Cluster with asynchronous={asynchronous}, but "
                f"cloud.asynchronous={cloud.asynchronous}, so the cluster will be"
                f"{cloud.asynchronous}"
            )

            asynchronous = cloud.asynchronous

        self.scheduler_comm: Optional[dask.distributed.rpc] = None

        # It's annoying that the user must pass in `asynchronous=True` to get an async Cluster object
        # But I can't think of a good alternative right now.
        self.cloud: CloudV2SyncAsync = cloud or CloudV2.current(asynchronous=asynchronous)
        # if cloud:
        #     self.cleanup_cloud = False
        #     self.cloud: CloudV2[IsAsynchronous] = cloud
        # else:
        #     self.cleanup_cloud = True
        #     self.cloud: CloudV2[IsAsynchronous] = CloudV2(asynchronous=asynchronous)

        # As of distributed 2021.12.0, deploy.Cluster has a ``loop`` attribute on the
        # base class. We add the attribute manually here for backwards compatibility.
        # TODO: if/when we set the minimum distributed version to be >= 2021.12.0,
        # remove this check.
        if DISTRIBUTED_VERSION >= Version("2021.12.0"):
            kwargs = {"loop": self.cloud.loop}
        else:
            kwargs = {}
            self.loop = self.cloud.loop

        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super().__init__(asynchronous, **kwargs)

        self.timeout = timeout if timeout is not None else self.cloud.default_cluster_timeout

        # Set cluster attributes from kwargs (first choice) or dask config

        self.private_to_creator = (
            dask.config.get("coiled.private-to-creator") if private_to_creator is None else private_to_creator
        )

        self.extra_worker_on_scheduler = extra_worker_on_scheduler
        self._worker_on_scheduler_name = None
        self.n_worker_specs_per_host = _n_worker_specs_per_host

        # FIXME what happens when no kwargs passed but coiled.software is set in dask config?
        self.software_environment = software or dask.config.get("coiled.software")
        self.software_container = container
        if not container and not software and not package_sync:
            self.package_sync = True

        self.worker_class = worker_class or dask.config.get("coiled.worker.class")
        self.worker_cpu = worker_cpu or cast(Union[int, List[int]], dask.config.get("coiled.worker.cpu"))

        if isinstance(worker_cpu, int) and worker_cpu <= 1:
            if not arm:
                raise ValueError("`worker_cpu` should be at least 2 for x86 instance types.")
            elif worker_cpu < 1:
                raise ValueError("`worker_cpu` should be at least 1 for arm instance types.")

        self.worker_memory = worker_memory or dask.config.get("coiled.worker.memory")
        # FIXME get these from dask config
        self.worker_vm_types = worker_vm_types
        self.worker_disk_size = worker_disk_size
        self.worker_disk_throughput = worker_disk_throughput
        self.worker_gpu_count = int(worker_gpu) if worker_gpu is not None else None
        self.worker_gpu_type = worker_gpu_type
        self.worker_options = {
            **(cast(dict, dask.config.get("coiled.worker-options", {}))),
            **(worker_options or {}),
        }

        self.scheduler_vm_types = scheduler_vm_types
        self.scheduler_class = scheduler_class or cast(str, dask.config.get("coiled.scheduler.class"))
        self.scheduler_cpu = scheduler_cpu or cast(Union[int, List[int]], dask.config.get("coiled.scheduler.cpu"))
        self.scheduler_memory = scheduler_memory or cast(
            Union[int, List[int]], dask.config.get("coiled.scheduler.memory")
        )
        self.scheduler_disk_size = scheduler_disk_size
        self.scheduler_options = {
            **(cast(dict, dask.config.get("coiled.scheduler-options", {}))),
            **(scheduler_options or {}),
        }

        # use dask config if kwarg not specified for scheduler gpu
        scheduler_gpu = scheduler_gpu if scheduler_gpu is not None else dask.config.get("coiled.scheduler.gpu")

        self._is_gpu_cluster = (
            # explicitly specified GPU (needed for GCP guest GPU)
            bool(worker_gpu or worker_gpu_type or scheduler_gpu)
            # or GPU bundled with explicitly specified instance type
            or any_gpu_instance_type(worker_vm_types)
            or any_gpu_instance_type(scheduler_vm_types)
        )

        if scheduler_gpu is None:
            # when not specified by user (via kwarg or config), default to GPU on scheduler if workers have GPU
            scheduler_gpu = True if self._is_gpu_cluster else False
        else:
            scheduler_gpu = bool(scheduler_gpu)
        self.scheduler_gpu = scheduler_gpu

        self.use_best_zone = use_best_zone

        self.spot_policy = spot_policy
        if compute_purchase_option:
            if spot_policy:
                raise ValueError(
                    "You specified both compute_purchase_option and spot_policy, "
                    "which serve the same purpose. Please specify only spot_policy."
                )
            else:
                self.spot_policy = compute_purchase_option

        self.name = name or cast(Optional[str], dask.config.get("coiled.name"))
        self.account = account
        self._start_n_workers = n_workers
        self._lock = None
        self._asynchronous = asynchronous
        self.shutdown_on_close = shutdown_on_close
        env_with_region = {"AWS_DEFAULT_REGION": self._get_aws_default_region(), **(environ or {})}
        self.environ = {k: str(v) for (k, v) in env_with_region.items() if v or v == ""}
        self.tags = {k: str(v) for (k, v) in (tags or {}).items() if v}
        self.frozen_dask_config = deepcopy(dask.config.config) if send_dask_config else {}
        self.credentials = CredentialsPreferred(credentials)
        self._credentials_duration_seconds = credentials_duration_seconds
        self._default_protocol = dask.config.get("coiled.protocol", "tls")
        self._wait_for_workers_arg = wait_for_workers
        self._last_logged_state_summary = None
        self._try_local_gcp_creds = True

        # these are sets of names of workers, only including workers in states that might eventually reach
        # a "started" state
        # they're used in our implementation of scale up/down (mostly inherited from coiled.Cluster)
        # and their corresponding properties are used in adaptive scaling (at least once we
        # make adaptive work with Cluster).
        #
        # (Adaptive expects attributes `requested` and `plan`, which we implement as properties below.)
        #
        # Some good places to learn about adaptive:
        # https://github.com/dask/distributed/blob/39024291e429d983d7b73064c209701b68f41f71/distributed/deploy/adaptive_core.py#L31-L43
        # https://github.com/dask/distributed/issues/5080
        self._requested: Set[str] = set()
        self._plan: Set[str] = set()

        self.cluster_id: Optional[int] = None
        self.use_scheduler_public_ip: bool = (
            dask.config.get("coiled.use_scheduler_public_ip", True)
            if use_scheduler_public_ip is None
            else use_scheduler_public_ip
        )
        self.use_dashboard_https: bool = (
            dask.config.get("coiled.use_dashboard_https", True) if use_dashboard_https is None else use_dashboard_https
        )

        self.backend_options = backend_options

        if allow_ingress_from is not None or allow_ssh is not None or scheduler_port is not None:
            if backend_options is not None and "ingress" in backend_options:
                raise ArgumentCombinationError(
                    "You cannot use `allow_ingress_from` or `allow_ssh` or `scheduler_port` when "
                    "`ingress` is also specified in `backend_options`."
                )
            firewall_kwargs = {
                "target": allow_ingress_from or "everyone",
                "ssh": False if allow_ssh is None else allow_ssh,
            }

            if scheduler_port is not None:
                firewall_kwargs["scheduler"] = scheduler_port
                self.scheduler_options["port"] = scheduler_port

            self.backend_options = self.backend_options or {}
            self.backend_options["ingress"] = cluster_firewall(**firewall_kwargs)["ingress"]  # type: ignore  # type: ignore

        if jupyter:
            self.scheduler_options["jupyter"] = True

        if idle_timeout:
            dask.utils.parse_timedelta(idle_timeout)  # fail fast if dask can't parse this timedelta
            self.scheduler_options["idle_timeout"] = idle_timeout

        if not self.asynchronous:
            # If we don't close the cluster, the user's ipython session gets spammed with
            # messages from distributed.
            #
            # Note that this doesn't solve all such spammy dead clusters (which is probably still
            # a problem), just spam created by clusters who failed initial creation.
            error = None
            try:
                self.sync(self._start)
            except (ClusterCreationError, InstanceTypeError) as e:
                error = e
                self.close()
                if self.cluster_id:
                    log_cluster_debug_info(self.cluster_id, self.account)
                raise e.with_traceback(None)
            except KeyboardInterrupt as e:
                error = e
                if self.cluster_id is not None and self.shutdown_on_close in (
                    True,
                    None,
                ):
                    logger.warning(f"Received KeyboardInterrupt, deleting cluster {self.cluster_id}")
                    self.cloud.delete_cluster(self.cluster_id, account=self.account)
                raise
            except Exception as e:
                error = e
                self.close()
                raise e.with_traceback(truncate_traceback(e.__traceback__))
            finally:
                if error:
                    self.sync(
                        self.cloud.add_interaction,
                        "cluster-create",
                        success=False,
                        additional_data={
                            **error_info_for_tracking(error),
                            **self._as_json_compatible(),
                        },
                    )
                else:
                    self.sync(
                        self.cloud.add_interaction,
                        "cluster-create",
                        success=True,
                        additional_data={
                            **self._as_json_compatible(),
                        },
                    )
            if self.start_adaptive:
                adaptive_max = 20
                logger.warn("Using adaptive scaling. To manually control the size of your cluster, use n_workers=.\n")
                self.adapt(minimum=n_workers, maximum=adaptive_max)

    @property
    def details_url(self):
        return get_details_url(self.cloud.server, self.account, self.cluster_id)

    @property
    def _grafana_url(self) -> Optional[str]:
        """for internal Coiled use"""
        if not self.cluster_id:
            return None

        details = self.cloud._get_cluster_details_synced(cluster_id=self.cluster_id, account=self.account)
        return get_grafana_url(details, account=self.account, cluster_id=self.cluster_id)

    def _ipython_display_(self: ClusterSyncAsync):
        cloud = self.cloud
        widget = None
        from IPython.display import display

        if use_rich_widget():
            widget = RichClusterWidget(server=self.cloud.server, account=self.account)

        if widget and self.cluster_id:
            # TODO: These synchronous calls may be too slow. They can be done concurrently
            cluster_details = cloud._get_cluster_details_synced(cluster_id=self.cluster_id, account=self.account)
            self.sync(self._update_cluster_status_logs, asynchronous=False)
            widget.update(cluster_details, self._cluster_status_logs)
            display(widget)

    def _repr_mimebundle_(self: ClusterSyncAsync, include: Iterable[str], exclude: Iterable[str], **kwargs):
        # In IPython 7.x This is called in an ipython terminal instead of
        # _ipython_display_ : https://github.com/ipython/ipython/pull/10249
        # In 8.x _ipython_display has been re-enabled in the terminal to
        # allow for rich outputs: https://github.com/ipython/ipython/pull/12315/files
        # So this function *should* only be calle  when in an ipython context using
        # IPython 7.x.
        cloud = self.cloud
        if use_rich_widget() and self.cluster_id:
            rich_widget = RichClusterWidget(server=self.cloud.server, account=self.account)
            cluster_details = cloud._get_cluster_details_synced(cluster_id=self.cluster_id, account=self.account)
            self.sync(self._update_cluster_status_logs, asynchronous=False)
            rich_widget.update(cluster_details, self._cluster_status_logs)
            return rich_widget._repr_mimebundle_(include, exclude, **kwargs)
        else:
            return {"text/plain": repr(self)}

    @track_context
    async def _get_cluster_vm_types_to_use(self):
        cloud = self.cloud
        if (self.worker_cpu or self.worker_memory) and not self.worker_vm_types:
            # match worker types by cpu and/or memory
            worker_vm_types_to_use = get_instance_type_from_cpu_memory(
                self.worker_cpu,
                self.worker_memory,
                gpus=self.worker_gpu_count,
                backend=await self._get_account_cloud_provider_name(),
                arch=self.arch.vm_arch,
            )
        elif (self.worker_cpu or self.worker_memory) and self.worker_vm_types:
            raise ArgumentCombinationError(_vm_type_cpu_memory_error_msg.format(kind="worker"))
        else:
            # get default types from dask config
            if self.worker_vm_types is None:
                self.worker_vm_types = dask.config.get("coiled.worker.vm-types")
            # accept string or list of strings
            if isinstance(self.worker_vm_types, str):
                self.worker_vm_types = [self.worker_vm_types]
            validate_vm_typing(self.worker_vm_types)
            worker_vm_types_to_use = self.worker_vm_types

        if (self.scheduler_cpu or self.scheduler_memory) and not self.scheduler_vm_types:
            # match scheduler types by cpu and/or memory
            scheduler_vm_types_to_use = get_instance_type_from_cpu_memory(
                self.scheduler_cpu,
                self.scheduler_memory,
                gpus=1 if self.scheduler_gpu else 0,
                backend=await self._get_account_cloud_provider_name(),
                arch=self.arch.vm_arch,
            )
        elif (self.scheduler_cpu or self.scheduler_memory) and self.scheduler_vm_types:
            raise ArgumentCombinationError(_vm_type_cpu_memory_error_msg.format(kind="scheduler"))
        else:
            # get default types from dask config
            if self.scheduler_vm_types is None:
                self.scheduler_vm_types = dask.config.get("coiled.scheduler.vm_types")
            # accept string or list of strings
            if isinstance(self.scheduler_vm_types, str):
                self.scheduler_vm_types = [self.scheduler_vm_types]
            validate_vm_typing(self.scheduler_vm_types)
            scheduler_vm_types_to_use = self.scheduler_vm_types

        # If we still don't have instance types, use the defaults
        if not scheduler_vm_types_to_use or not worker_vm_types_to_use:
            provider = await self._get_account_cloud_provider_name()

            if not self.scheduler_gpu and not self.worker_gpu_count:
                # When no GPUs, use same default for scheduler and workers
                default_vm_types = await cloud._get_default_instance_types(
                    provider=provider,
                    gpu=False,
                    arch=self.arch.vm_arch,
                )
                scheduler_vm_types_to_use = scheduler_vm_types_to_use or default_vm_types
                worker_vm_types_to_use = worker_vm_types_to_use or default_vm_types
            else:
                # GPUs so there might be different defaults for scheduler/workers
                if not scheduler_vm_types_to_use:
                    scheduler_vm_types_to_use = get_instance_type_from_cpu_memory(
                        gpus=1 if self.scheduler_gpu else 0,
                        backend=await self._get_account_cloud_provider_name(),
                        arch=self.arch.vm_arch,
                    )
                if not worker_vm_types_to_use:
                    worker_vm_types_to_use = get_instance_type_from_cpu_memory(
                        gpus=self.worker_gpu_count,
                        arch=self.arch.vm_arch,
                    )

        return scheduler_vm_types_to_use, worker_vm_types_to_use

    @track_context
    async def _get_account_cloud_provider_name(self) -> str:
        if not hasattr(self, "_cached_account_cloud_provider_name"):
            self._cached_account_cloud_provider_name = await self.cloud.get_account_provider_name(account=self.account)

        return self._cached_account_cloud_provider_name

    @track_context
    async def _check_create_or_reuse(self):
        cloud = self.cloud
        if self.name:
            try:
                self.cluster_id = await cloud._get_cluster_by_name(
                    name=self.name,
                    account=self.account,
                )
            except DoesNotExist:
                should_create = True
            else:
                logger.info(f"Using existing cluster: '{self.name} (id: {self.cluster_id})'")
                should_create = False
        else:
            should_create = True
            self.name = self.name or (self.account or cloud.default_account) + "-" + short_random_string()
        return should_create

    @track_context
    async def _determine_senv(
        self,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        gpu_enabled: bool = False,
    ) -> Optional[int]:
        # For package sync, this is where we scrape local environment, determine
        # what to install on cluster, and build/upload wheels as needed.
        if self.package_sync:
            progress = Progress(
                TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn()
            )
            if self.show_widget and use_rich_widget():
                live = Live(Panel(progress, title="[green]Package Sync", width=CONSOLE_WIDTH))

            else:
                live = contextlib.nullcontext()
            with live:
                with simple_progress("Fetching latest package priorities", progress):
                    logger.info("Resolving your local Python environment...")
                    package_levels = await self.cloud._fetch_package_levels()
                package_level_lookup = {
                    (pkg["name"], pkg["source"]): PackageLevelEnum(pkg["level"]) for pkg in package_levels
                }
                if self.package_sync_ignore:
                    for package in self.package_sync_ignore:
                        package_level_lookup[(package, "conda")] = PackageLevelEnum.IGNORE
                        package_level_lookup[(package, "pip")] = PackageLevelEnum.IGNORE
                approximation = await create_environment_approximation(
                    cloud=self.cloud,
                    only=self.package_sync_only,
                    priorities=package_level_lookup,
                    strict=self.package_sync_strict,
                    progress=progress,
                    architecture=architecture,
                )

                if not self.package_sync_only:
                    # if we're not operating on a subset, check
                    # all the coiled defined critical packages are present
                    packages_by_name: Dict[str, ResolvedPackageInfo] = {p["name"]: p for p in approximation}
                    self._check_halting_issues(package_levels, packages_by_name)
                packages_with_errors = [
                    (
                        pkg,
                        package_level_lookup.get(
                            (
                                (cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]),
                                pkg["source"],
                            ),
                            PackageLevelEnum.WARN,
                        ),
                    )
                    for pkg in approximation
                    if pkg["error"]
                ]
                for pkg_with_error, level in packages_with_errors:
                    if level >= PackageLevelEnum.WARN:
                        logfunc = logger.warn
                    else:
                        logfunc = logger.info
                    logfunc(f"Package - {pkg_with_error['name']}, {pkg_with_error['error']}")
                packages_with_notes = [
                    pkg
                    for pkg in approximation
                    if (
                        pkg["note"]
                        and (
                            package_level_lookup.get(
                                (
                                    (cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]),
                                    pkg["source"],
                                ),
                                PackageLevelEnum.WARN,
                            )
                            > PackageLevelEnum.IGNORE
                        )
                    )
                ]
                for pkg_with_note in packages_with_notes:
                    logger.debug(f"Package - {pkg_with_note['name']}, {pkg_with_note['note']}")

                await self._get_account_cloud_provider_name()
                package_sync_env_alias = await self.cloud._create_package_sync_env(
                    packages=approximation,
                    account=self.account,
                    progress=progress,
                    gpu_enabled=gpu_enabled,
                    architecture=architecture,
                    # This is okay because we will default to account
                    # default region in declarative service create_software_environment
                    region_name=self.backend_options.get("region_name") if self.backend_options else None,
                )
                package_sync_env = package_sync_env_alias["id"]
            if use_rich_widget() and self.show_widget:
                print_rich_package_table(packages_with_notes, packages_with_errors)

            logger.debug(f"Environment capture complete, {package_sync_env}")
        else:
            package_sync_env = None

        return package_sync_env

    @track_context
    def _check_halting_issues(
        self,
        package_levels: List[PackageLevel],
        packages_by_name: Dict[str, ResolvedPackageInfo],
    ):
        critical_packages = [pkg["name"] for pkg in package_levels if pkg["level"] == PackageLevelEnum.CRITICAL]
        halting_failures = []
        for critical_package in critical_packages:
            if critical_package not in packages_by_name:
                problem: ResolvedPackageInfo = {
                    "name": critical_package,
                    "sdist": None,
                    "source": "pip",
                    "channel": None,
                    "conda_name": critical_package,
                    "client_version": "n/a",
                    "specifier": "n/a",
                    "include": False,
                    "note": None,
                    "error": f"Could not detect package locally, please install {critical_package}",
                    "md5": None,
                }
                halting_failures.append(problem)
            elif not packages_by_name[critical_package]["include"]:
                halting_failures.append(packages_by_name[critical_package])
        for package_level in package_levels:
            package = packages_by_name.get(package_level["name"])
            if package and package["error"]:
                if package_level["level"] > self.package_sync_fail_on or self.package_sync_strict:
                    halting_failures.append(package)
        if halting_failures:
            # fall back to the note if no error is present
            # this only really happens if a user specified
            # a critical package to ignore
            failure_str = ", ".join([f'{pkg["name"]} - {pkg["error"] or pkg["note"]}' for pkg in halting_failures])
            raise RuntimeError(
                f"""Issues with critical packages: {failure_str}

Your software environment has conflicting dependency requirements.

Consider creating a new environment.

By specifying your packages at once, you're more likely to get a consistent set of versions.

If you use conda:

    conda create -n myenv -c conda-forge coiled package1 package2 package3

If you use pip/venv, create a new environment and then:

    pip install coiled package1 package2 package3
or
    pip install -r requirements.txt

If that does not solve your issue, please contact support@coiled.io."""
            )

    @track_context
    async def _attach_to_cluster(self, is_new_cluster: bool):
        assert self.cluster_id

        # this is what waits for the cluster to be "ready"
        await self._wait_until_ready(is_new_cluster)

        results = await asyncio.gather(
            *[
                self._set_plan_requested(),
                self.cloud._security(
                    cluster_id=self.cluster_id,
                    account=self.account,
                ),
            ]
        )
        self.security, security_info = results[1]

        self._proxy = bool(self.security.extra_conn_args)
        self._dashboard_address = security_info["dashboard_address"]

        if self.use_scheduler_public_ip:
            rpc_address = security_info["public_address"]
        else:
            rpc_address = security_info["private_address"]
            logger.info(f"Connecting to scheduler on its internal address: {rpc_address}")

        try:
            self.scheduler_comm = dask.distributed.rpc(
                rpc_address,
                connection_args=self.security.get_connection_args("client"),
            )
            await self._send_credentials()
        except IOError as e:
            if "Timed out" in str(e):
                raise RuntimeError(
                    "Unable to connect to Dask cluster. This may be due "
                    "to different versions of `dask` and `distributed` "
                    "locally and remotely.\n\n"
                    f"You are using distributed={DISTRIBUTED_VERSION} locally.\n\n"
                    "With pip, you can upgrade to the latest with:\n\n"
                    "\tpip install --upgrade dask distributed"
                )
            raise

    @track_context
    async def _start(self):
        did_error = False
        cluster_created = False

        await self.cloud
        try:
            cloud = self.cloud
            self.account = self.account or self.cloud.default_account

            # check_create_or_reuse has the side effect of creating a name
            # if none is assigned
            should_try_create = await self._check_create_or_reuse()
            self.name = self.name or (self.account or cloud.default_account) + "-" + short_random_string()
            assert self.name

            # Set shutdown_on_close here instead of in __init__ to make sure
            # the dask config default isn't used when we are reusing a cluster
            if self.shutdown_on_close is None:
                self.shutdown_on_close = should_try_create and dask.config.get("coiled.shutdown-on-close")

            if should_try_create:
                (
                    scheduler_vm_types_to_use,
                    worker_vm_types_to_use,
                ) = await self._get_cluster_vm_types_to_use()

                user_provider = await self._get_account_cloud_provider_name()

                # Update backend options for cluster based on the friendlier kwargs
                if self.scheduler_gpu:
                    if user_provider == "gcp":
                        self.backend_options = {
                            **GCP_SCHEDULER_GPU,
                            **(self.backend_options or {}),
                        }
                if self.use_best_zone:
                    self.backend_options = {
                        **(self.backend_options or {}),
                        "multizone": True,
                    }
                if self.spot_policy:
                    purchase_configs = {
                        "on-demand": {"spot": False},
                        "spot": {
                            "spot": True,
                            "spot_on_demand_fallback": False,
                        },
                        "spot_with_fallback": {
                            "spot": True,
                            "spot_on_demand_fallback": True,
                        },
                    }

                    if self.spot_policy not in purchase_configs:
                        valid_options = ", ".join(purchase_configs.keys())
                        raise ValueError(
                            f"{self.spot_policy} is not a valid spot_policy; " f"valid options are: {valid_options}"
                        )

                    self.backend_options = {
                        **(self.backend_options or {}),
                        **purchase_configs[self.spot_policy],
                    }

                # Elsewhere (in _wait_until_ready) we actually decide how many workers to wait for,
                # in a way that's unified/correct for both the "should_create" case and the case
                # where a cluster already exists.
                #
                # However, we should check here to make sure _wait_for_workers_arg is valid to
                # avoid creating the cluster if it's not valid.
                #
                # (We can't do this check earlier because we don't know until now if we're
                # creating a cluster, and if we're not then "_start_n_workers" may be the wrong
                # number of workers...)
                parse_wait_for_workers(self._start_n_workers, self._wait_for_workers_arg)

                # Determine software environment (legacy or package sync)
                architecture = (
                    ArchitectureTypesEnum.ARM64
                    if (
                        (
                            user_provider == "aws"
                            and all(
                                re.search(r"^\w+\d.*g.*", vm_type.split(".")[0], flags=re.IGNORECASE)
                                for vm_type in chain(scheduler_vm_types_to_use, worker_vm_types_to_use)
                            )
                        )
                        or (
                            user_provider == "gcp"
                            and all(
                                vm_type.split("-")[0].lower() == "t2a"
                                for vm_type in chain(scheduler_vm_types_to_use, worker_vm_types_to_use)
                            )
                        )
                    )
                    else ArchitectureTypesEnum.X86_64
                )

                # `architecture` is set to ARM64 iff *all* instances are ARM,
                # so when architecture is X86_64 that could mean all instances are x86
                # or it could mean that there's a mix (which we want to reject).
                if architecture == ArchitectureTypesEnum.ARM64:
                    self.arch = ArchitectureTypesEnum.ARM64

                # This check ensures that if the user asked for ARM cluster (using the `arm` kwarg),
                # then they didn't also explicitly specify x86 instance type.
                # (It also catches if our code to pick ARM instances types returns an x86 instance type.)
                if architecture != self.arch:
                    # TODO (future PR) more specific error about which instance type doesn't match
                    raise RuntimeError(
                        f"Requested cluster architecture ({self.arch.vm_arch}) does not match "
                        f"architecture of some instance types ({scheduler_vm_types_to_use}, {worker_vm_types_to_use})."
                    )
                # TODO (future PR) still use strict mode for GPU cluster if local env also has GPU
                if (
                    platform.machine() == architecture
                    and platform.system() == "Linux"
                    and not is_system_python()
                    and not self._is_gpu_cluster
                    and not self.package_sync_ignore
                ):
                    self.package_sync_strict = True

                # create an ad hoc software environment if container was specified
                if self.software_container:
                    # make a valid software env name unique for this container
                    image_and_tag = self.software_container.split("/")[-1]
                    uri_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.software_container))
                    container_senv_name = re.sub(
                        r"[^A-Za-z0-9-_]", "_", f"{image_and_tag}-{self.arch}-{uri_uuid}"
                    ).lower()

                    await cloud._create_software_environment(
                        name=container_senv_name,
                        container=self.software_container,
                        account=self.account,
                        architecture=self.arch,
                        region_name=self.backend_options.get("region_name") if self.backend_options else None,
                    )
                    self.software_environment = container_senv_name

                # Validate software environment name, setting `can_have_revision` to False since
                # we don't seem to be using this yet.
                if not self.package_sync:
                    parse_identifier(
                        self.software_environment,
                        property_name="software_environment",
                        can_have_revision=False,
                    )

                senv_v2_id = await self._determine_senv(architecture=architecture, gpu_enabled=self._is_gpu_cluster)

                self.cluster_id, cluster_existed = await cloud._create_cluster(
                    account=self.account,
                    name=self.name,
                    workers=self._start_n_workers,
                    software_environment=self.software_environment,
                    worker_class=self.worker_class,
                    worker_options=self.worker_options,
                    worker_disk_size=self.worker_disk_size,
                    worker_disk_throughput=self.worker_disk_throughput,
                    gcp_worker_gpu_type=self.worker_gpu_type,
                    gcp_worker_gpu_count=self.worker_gpu_count,
                    scheduler_disk_size=self.scheduler_disk_size,
                    scheduler_class=self.scheduler_class,
                    scheduler_options=self.scheduler_options,
                    environ=self.environ,
                    tags=self.tags,
                    dask_config=self.frozen_dask_config,
                    scheduler_vm_types=scheduler_vm_types_to_use,
                    worker_vm_types=worker_vm_types_to_use,
                    backend_options=self.backend_options,
                    use_scheduler_public_ip=self.use_scheduler_public_ip,
                    use_dashboard_https=self.use_dashboard_https,
                    senv_v2_id=senv_v2_id,
                    private_to_creator=self.private_to_creator,
                    extra_worker_on_scheduler=self.extra_worker_on_scheduler,
                    n_worker_specs_per_host=self.n_worker_specs_per_host,
                )
                cluster_created = not cluster_existed

            if not self.cluster_id:
                raise RuntimeError(f"Failed to find/create cluster {self.name}")

            if cluster_created:
                logger.info(
                    f"Creating Cluster (name: {self.name}, {self.details_url} ). This usually takes 1-2 minutes..."
                )
            else:
                logger.info(f"Attaching to existing cluster (name: {self.name}, {self.details_url} )")

            await self._attach_to_cluster(is_new_cluster=cluster_created)
            await super()._start()

            # Set adaptive maximum value based on available config and user quota
        except Exception as e:
            if self._asynchronous:
                did_error = True
                asyncio.create_task(
                    self.cloud.add_interaction(
                        "cluster-create",
                        success=False,
                        additional_data={
                            **error_info_for_tracking(e),
                            **self._as_json_compatible(),
                        },
                    )
                )
            raise
        finally:
            if self._asynchronous and not did_error:
                asyncio.create_task(
                    self.cloud.add_interaction(
                        "cluster-create",
                        success=True,
                        additional_data={
                            **self._as_json_compatible(),
                        },
                    )
                )

    def _as_json_compatible(self):
        # the typecasting here is to avoid accidentally
        # submitting something passed in that is not json serializable
        # (user error may cause this)
        return {
            "name": str(self.name),
            "software_environment": str(self.software_environment),
            "show_widget": bool(self.show_widget),
            "async": bool(self._asynchronous),
            "worker_class": str(self.worker_class),
            "worker_cpu": str(self.worker_cpu),
            "worker_memory": str(self.worker_memory),
            "worker_vm_types": str(self.worker_vm_types),
            "worker_gpu_count": str(self.worker_gpu_count),
            "worker_gpu_type": str(self.worker_gpu_type),
            "scheduler_class": str(self.scheduler_class),
            "scheduler_cpu": str(self.scheduler_class),
            "scheduler_memory": str(self.scheduler_memory),
            "scheduler_vm_types": str(self.scheduler_vm_types),
            "n_workers": int(self._start_n_workers),
            "shutdown_on_close": bool(self.shutdown_on_close),
            "use_scheduler_public_ip": bool(self.use_scheduler_public_ip),
            "use_dashboard_https": bool(self.use_dashboard_https),
            "package_sync": bool(self.package_sync),
            "package_sync_ignore": str(self.package_sync_ignore) if self.package_sync_ignore else False,
            "execution_context": EXECUTION_CONTEXT,
            "account": self.account,
            "timeout": self.timeout,
            "wait_for_workers": self._wait_for_workers_arg,
            "cluster_id": self.cluster_id,
            "backend_options": self.backend_options,
            "scheduler_gpu": self.scheduler_gpu,
            "use_best_zone": self.use_best_zone,
            "spot_policy": self.spot_policy,
            "start_adaptive": self.start_adaptive,
            "errored_worker_count": self.errored_worker_count,
            # NOTE: this is not a measure of the CLUSTER life time
            # just a measure of how long this object has been around
            "cluster_object_life": str(datetime.datetime.now() - self.init_time),
        }

    def _maybe_log_summary(self, cluster_details):
        now = time.time()
        if self._last_logged_state_summary is None or now > self._last_logged_state_summary + 5:
            logger.debug(summarize_status(cluster_details))
            self._last_logged_state_summary = now

    @track_context
    async def _wait_until_ready(self, is_new_cluster: bool) -> None:
        cloud = self.cloud
        cluster_id = self._assert_cluster_id()
        timeout_at = (
            datetime.datetime.now() + datetime.timedelta(seconds=self.timeout) if self.timeout is not None else None
        )
        self._latest_dt_seen = None

        if self.custom_widget:
            widget = self.custom_widget
            ctx = contextlib.nullcontext()
        elif self.show_widget and use_rich_widget():
            widget = RichClusterWidget(
                n_workers=self._start_n_workers,
                server=self.cloud.server,
                account=self.account,
            )
            ctx = widget
        else:
            widget = None
            ctx = contextlib.nullcontext()

        num_workers_to_wait_for = None
        with ctx:
            while True:
                cluster_details = await cloud._get_cluster_details(cluster_id=cluster_id, account=self.account)
                # Computing num_workers_to_wait_for inside the while loop is kinda goofy, but I don't want to add an
                # extra _get_cluster_details call right now since that endpoint can be very slow for big clusters.
                # Let's optimize it, and then move this code up outside the loop.

                if num_workers_to_wait_for is None:
                    cluster_desired_workers = cluster_details["desired_workers"]
                    num_workers_to_wait_for = parse_wait_for_workers(
                        cluster_desired_workers, self._wait_for_workers_arg
                    )
                    if not is_new_cluster:
                        if self.start_adaptive:
                            # When re-attaching to existing cluster without specifying n_workers,
                            # we don't want to start adaptive (which we'd do otherwise when n_workers isn't specified)
                            # and we also don't want to show message that we're ignoring n_workers (since in this case
                            # it was set as default because n_workers was unspecified).
                            self.start_adaptive = False
                        elif self._start_n_workers != cluster_desired_workers:
                            logging.warning(
                                f"Ignoring your request for {self._start_n_workers} workers since you are "
                                f"connecting to a cluster that had been requested with {cluster_desired_workers} "
                                "workers"
                            )

                await self._update_cluster_status_logs()
                self._maybe_log_summary(cluster_details)

                if widget:
                    widget.update(
                        cluster_details,
                        self._cluster_status_logs,
                    )

                cluster_state = ClusterStateEnum(cluster_details["current_state"]["state"])
                reason = cluster_details["current_state"]["reason"]

                scheduler_current_state = cluster_details["scheduler"]["current_state"]
                scheduler_state = ProcessStateEnum(scheduler_current_state["state"])
                if cluster_details["scheduler"].get("instance"):
                    scheduler_instance_state = InstanceStateEnum(
                        cluster_details["scheduler"]["instance"]["current_state"]["state"]
                    )
                else:
                    scheduler_instance_state = InstanceStateEnum.queued
                worker_current_states = [w["current_state"] for w in cluster_details["workers"]]
                ready_worker_current = [
                    current
                    for current in worker_current_states
                    if ProcessStateEnum(current["state"]) == ProcessStateEnum.started
                ]
                self.errored_worker_count = sum(
                    [
                        1
                        for current in worker_current_states
                        if ProcessStateEnum(current["state"]) == ProcessStateEnum.error
                    ]
                )
                starting_workers = sum(
                    [
                        1
                        for current in worker_current_states
                        if ProcessStateEnum(current["state"])
                        in [
                            ProcessStateEnum.starting,
                            ProcessStateEnum.pending,
                        ]
                    ]
                )

                if scheduler_state == ProcessStateEnum.started and scheduler_instance_state in [
                    InstanceStateEnum.ready,
                    InstanceStateEnum.started,
                ]:
                    scheduler_ready = True
                    scheduler_reason_not_ready = ""
                else:
                    scheduler_ready = False
                    scheduler_reason_not_ready = "Scheduler not ready."

                n_workers_ready = len(ready_worker_current)

                final_update = None
                if n_workers_ready >= num_workers_to_wait_for:
                    if n_workers_ready == self._start_n_workers:
                        final_update = "All workers ready."
                    else:
                        final_update = "Most of your workers have arrived. Cluster ready for use."

                    enough_workers_ready = True
                    workers_reason_not_ready = ""
                else:
                    enough_workers_ready = False
                    workers_reason_not_ready = (
                        f"Only {len(ready_worker_current)} workers ready "
                        f"(was waiting for at least {num_workers_to_wait_for}). "
                    )

                # Check if cluster is ready to return to user in a good state
                if scheduler_ready and enough_workers_ready:
                    assert final_update is not None
                    if widget:
                        widget.update(
                            cluster_details,
                            self._cluster_status_logs,
                            final_update=final_update,
                        )
                    logger.debug(summarize_status(cluster_details))
                    return
                else:
                    reason_not_ready = scheduler_reason_not_ready if not scheduler_ready else workers_reason_not_ready
                    if cluster_state in (
                        ClusterStateEnum.error,
                        ClusterStateEnum.stopped,
                        ClusterStateEnum.stopping,
                    ):
                        # this cluster will never become ready; raise an exception
                        error = f"Cluster status is {cluster_state.value} (reason: {reason})"
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=error,
                            )
                        logger.debug(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            error,
                            cluster_id=self.cluster_id,
                        )
                    elif cluster_state == ClusterStateEnum.ready:
                        # (cluster state "ready" means all worked either started or errored, so
                        # this cluster will never have all the workers we want)
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=reason_not_ready,
                            )
                        logger.debug(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            reason_not_ready,
                            cluster_id=self.cluster_id,
                        )
                    elif (starting_workers + n_workers_ready) < num_workers_to_wait_for:
                        # including workers that are starting, cluster cannot get to the number
                        # of desired ready workers (because some workers have already errored),
                        logger.debug(summarize_status(cluster_details))

                        message = (
                            f"Cluster was waiting for {num_workers_to_wait_for} workers but "
                            f"{self.errored_worker_count} (of {self._start_n_workers}) workers have already failed. "
                            "You could try requesting fewer workers or adjust `wait_for_workers` if fewer workers "
                            "would be acceptable."
                        )
                        errors = group_worker_errors(cluster_details)
                        if errors:
                            header = "Failure Reasons\n" "---------------"
                            message = f"{message}\n\n{header}"
                            # show error that affected the most workers first
                            for error in sorted(errors, key=lambda k: -errors[k]):
                                n_affected = errors[error]
                                plural = "" if n_affected == 1 else "s"
                                error_message = f"{error}\n\t(error affected {n_affected} worker{plural})"
                                message = f"{message}\n\n{error_message}"

                        raise ClusterCreationError(
                            message,
                            cluster_id=self.cluster_id,
                        )
                    elif timeout_at is not None and datetime.datetime.now() > timeout_at:
                        error = "User-specified timeout expired: " + reason_not_ready
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=error,
                            )
                        logger.debug(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            error,
                            cluster_id=self.cluster_id,
                        )

                    else:
                        await asyncio.sleep(1.0)

    async def _update_cluster_status_logs(self):
        cluster_id = self._assert_cluster_id()
        states_by_type = await self.cloud._get_cluster_states_declarative(
            cluster_id, self.account, start_time=self._latest_dt_seen
        )
        states = flatten_log_states(states_by_type)
        if states:
            if not self.custom_widget and (not self.show_widget or EXECUTION_CONTEXT == "terminal"):
                log_states(states)
            self._latest_dt_seen = states[-1].updated
            self._cluster_status_logs.extend(states)

    def _assert_cluster_id(self) -> int:
        if self.cluster_id is None:
            raise RuntimeError("'cluster_id' is not set, perhaps the cluster hasn't been created yet")
        return self.cluster_id

    def cwi_logs_url(self):
        if self.cluster_id is None:
            raise ValueError("cluster_id is None. Cannot get CloudWatch link without a cluster")

        # kinda hacky, probably something as important as region ought to be an attribute on the
        # cluster itself already and not require an API call
        cluster_details = self.cloud._get_cluster_details_synced(cluster_id=self.cluster_id, account=self.account)
        if cluster_details["backend_type"] != "vm_aws":
            raise ValueError("Sorry, the cwi_logs_url only works for AWS clusters.")
        region = cluster_details["cluster_options"]["region_name"]

        return cloudwatch_url(self.account, self.name, region)

    def details(self):
        if self.cluster_id is None:
            raise ValueError("cluster_id is None. Cannot get details without a cluster")
        return self.cloud.cluster_details(cluster_id=self.cluster_id, account=self.account)

    async def _set_plan_requested(self):
        eventually_maybe_good_statuses = [
            ProcessStateEnum.starting,
            ProcessStateEnum.pending,
            ProcessStateEnum.started,
        ]
        assert self.account
        assert self.cluster_id
        eventually_maybe_good_workers = await self.cloud._get_worker_names(
            account=self.account,
            cluster_id=self.cluster_id,
            statuses=eventually_maybe_good_statuses,
        )

        # scale (including adaptive) relies on `plan` and `requested` and these (on Coiled)
        # are set based on the control-plane's view of what workers there are, so if we have
        # extra worker on the scheduler (which isn't tracked separately by control-plane)
        # we need to include that here.
        if self.extra_worker_on_scheduler:
            # get the actual name of worker on scheduler if we haven't gotten it yet
            if not self._worker_on_scheduler_name:
                worker_on_scheduler = [worker for worker in self.observed if "scheduler" in worker]
                if worker_on_scheduler:
                    self._worker_on_scheduler_name = worker_on_scheduler[0]
            # if we have actual name, use it, otherwise use fake name for now
            if self._worker_on_scheduler_name:
                eventually_maybe_good_workers.add(self._worker_on_scheduler_name)
            else:
                eventually_maybe_good_workers.add("extra-worker-on-scheduler")

        self._plan = eventually_maybe_good_workers
        self._requested = eventually_maybe_good_workers

    @track_context
    async def _scale(self, n: int) -> None:
        if not self.cluster_id:
            raise ValueError("No cluster available to scale!")

        await self._set_plan_requested()  # need to update our understanding of current workers before scaling
        logger.debug(f"current _plan: {self._plan}")

        recommendations = await self.recommendations(n)
        logger.debug(f"scale recommendations: {recommendations}")

        return await self._apply_scaling_recommendations(recommendations)

    @track_context
    async def scale_up(self, n: int, reason: Optional[str] = None) -> None:
        """
        Scales up *to* a target number of ``n`` workers

        It's documented that scale_up should scale up to a certain target, not scale up BY a certain amount:

        https://github.com/dask/distributed/blob/main/distributed/deploy/adaptive_core.py#L60
        """
        if not self.cluster_id:
            raise ValueError("No cluster available to scale! " "Check cluster was not closed by another process.")
        target = n - len(self.plan)
        response = await self.cloud._scale_up(
            account=self.account,
            cluster_id=self.cluster_id,
            n=target,
            reason=reason,
        )
        if response:
            self._plan.update(set(response.get("workers", [])))
            self._requested.update(set(response.get("workers", [])))

    @track_context
    async def _close(self, force_shutdown: bool = False) -> None:
        # My small changes to _close probably make sense for legacy Cluster too, but I don't want to carefully
        # test them, so copying this method over.

        with suppress(AttributeError):
            self._adaptive.stop()  # type: ignore

        # Stop here because otherwise we get intermittent `OSError: Timed out` when
        # deleting cluster takes a while and callback tries to poll cluster status.
        for pc in self.periodic_callbacks.values():
            pc.stop()

        if hasattr(self, "cluster_id") and self.cluster_id:
            # If the initial create call failed, we don't have a cluster ID.
            # But the rest of this method (at least calling distributed.deploy.Cluster.close)
            # is important.
            if force_shutdown or self.shutdown_on_close in (True, None):
                await self.cloud._delete_cluster(
                    account=self.account,
                    cluster_id=self.cluster_id,
                )
        await super()._close()

    @property
    def requested(self):
        return self._requested

    @property
    def plan(self):
        return self._plan

    @overload
    def sync(
        self: Cluster[Sync],
        func: Callable[..., Awaitable[_T]],
        *args,
        asynchronous: Union[Sync, Literal[None]] = None,
        callback_timeout=None,
        **kwargs,
    ) -> _T:
        ...

    @overload
    def sync(
        self: Cluster[Async],
        func: Callable[..., Awaitable[_T]],
        *args,
        asynchronous: Union[bool, Literal[None]] = None,
        callback_timeout=None,
        **kwargs,
    ) -> Coroutine[Any, Any, _T]:
        ...

    def sync(
        self,
        func: Callable[..., Awaitable[_T]],
        *args,
        asynchronous: Optional[bool] = None,
        callback_timeout=None,
        **kwargs,
    ) -> Union[_T, Coroutine[Any, Any, _T]]:
        return cast(
            Union[_T, Coroutine[Any, Any, _T]],
            super().sync(
                func,
                *args,
                asynchronous=asynchronous,
                callback_timeout=callback_timeout,
                **kwargs,
            ),
        )

    def _ensure_scheduler_comm(self) -> dask.distributed.rpc:
        """
        Guard to make sure that the scheduler comm exists before trying to use it.
        """
        if not self.scheduler_comm:
            raise RuntimeError("Scheduler comm is not set, have you been disconnected from Coiled?")
        return self.scheduler_comm

    @track_context
    async def _wait_for_workers(
        self,
        n_workers,
        timeout=None,
        err_msg=None,
    ) -> None:
        if timeout is None:
            deadline = None
        else:
            timeout = dask.utils.parse_timedelta(timeout, "s")
            deadline = time.time() + timeout if timeout else None
        while n_workers and len(self.scheduler_info["workers"]) < n_workers:
            if deadline and time.time() > deadline:
                err_msg = err_msg or (
                    f"Timed out after {timeout} seconds waiting for {n_workers} workers to arrive, "
                    "check your notifications with coiled.get_notifications() for further details"
                )
                raise TimeoutError(err_msg)
            await asyncio.sleep(1)

    @staticmethod
    def _get_aws_default_region() -> Optional[str]:
        try:
            from boto3.session import Session

            region_name = Session().region_name
            return str(region_name) if region_name else None
        except Exception:
            pass
        return None

    @staticmethod
    def _sync_get_aws_local_session_token(
        duration_seconds: Optional[int] = None,
    ) -> AWSSessionCredentials:
        token_creds = AWSSessionCredentials(
            AccessKeyId="",
            SecretAccessKey="",
            SessionToken=None,
            Expiration=None,
            DefaultRegion=None,
        )
        try:
            from boto3.session import Session

            session = Session()

            sts = session.client("sts")
            try:
                kwargs = {"DurationSeconds": duration_seconds} if duration_seconds else {}
                credentials = sts.get_session_token(**kwargs)

                credentials = credentials["Credentials"]
                token_creds = AWSSessionCredentials(
                    AccessKeyId=credentials.get("AccessKeyId", ""),
                    SecretAccessKey=credentials.get("SecretAccessKey", ""),
                    SessionToken=credentials.get("SessionToken"),
                    Expiration=credentials.get("Expiration"),
                    DefaultRegion=session.region_name,
                )
            except botocore.exceptions.ClientError as e:
                if "session credentials" in str(e):
                    # Credentials are already an STS token, which gives us this error:
                    # > Cannot call GetSessionToken with session credentials
                    # In this case we'll just use the existing STS token for the active, local session.
                    # Note that in some cases this will have a shorter TTL than the default 12 hour tokens.
                    credentials = session.get_credentials()
                    frozen_creds = credentials.get_frozen_credentials()

                    expiration = credentials._expiry_time if hasattr(credentials, "_expiry_time") else None

                    logger.debug(
                        "Local AWS session is already using STS token, this will be used since we can't "
                        f"generate a new STS token from this. Expiration: {expiration}."
                    )

                    token_creds = AWSSessionCredentials(
                        AccessKeyId=frozen_creds.access_key,
                        SecretAccessKey=frozen_creds.secret_key,
                        SessionToken=frozen_creds.token,
                        Expiration=expiration,
                        DefaultRegion=session.region_name,
                    )

        except (
            botocore.exceptions.ProfileNotFound,
            botocore.exceptions.NoCredentialsError,
        ):
            # no AWS credentials (maybe not running against AWS?), fail gracefully
            pass
        except Exception as e:
            # for some aiobotocore versions (e.g. 2.3.4) we get one of these errors
            # rather than NoCredentialsError
            if "Could not connect to the endpoint URL" in str(e):
                pass
            elif "Connect timeout on endpoint URL" in str(e):
                pass
            else:
                # warn, but don't crash
                logger.warning(f"Error getting STS token from client AWS session: {e}")

        return token_creds

    async def _get_aws_local_session_token(
        self,
        duration_seconds: Optional[int] = None,
    ) -> AWSSessionCredentials:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._sync_get_aws_local_session_token, duration_seconds)

    def _has_gcp_auth_installed(self) -> bool:
        try:
            import google.auth  # type: ignore # noqa F401
            from google.auth.transport.requests import Request  # type: ignore # noqa F401

            return True
        except ImportError:
            self._try_local_gcp_creds = False
            return False

    @staticmethod
    def _get_gcp_local_session_token() -> dict:
        auth_logger = None
        comp_logger = None
        auth_logger_level = 0
        comp_logger_level = 0

        try:
            import google.auth
            from google.auth.transport.requests import Request

            auth_logger = logging.getLogger("google.auth._default")
            comp_logger = logging.getLogger("google.auth.compute_engine._metadata")
            auth_logger_level = auth_logger.level
            comp_logger_level = comp_logger.level
            auth_logger.setLevel(logging.ERROR)
            comp_logger.setLevel(logging.ERROR)

            # get token from local auth
            local_creds, project = google.auth.default()
            local_creds.refresh(Request())

            auth_logger.setLevel(auth_logger_level)
            comp_logger.setLevel(comp_logger_level)

            return {
                "token": local_creds.token,
                "project": project,
                "expiry": local_creds.expiry.replace(tzinfo=datetime.timezone.utc),
            }
        except Exception as e:
            if "default credentials were not found" not in str(e):
                logger.warning(f"Error getting token from client GCP session: {e}")
        finally:
            if auth_logger:
                auth_logger.setLevel(auth_logger_level)
            if comp_logger:
                comp_logger.setLevel(comp_logger_level)

        return {}

    def set_keepalive(self, keepalive):
        """
        Set how long to keep cluster running if all the clients have disconnected.

        This is a way to shut down no-longer-used cluster, in additional to dask idle timeout.
        With no keepalive set, cluster will not shut down on account of clients going away.

        Arguments:
            keepalive: duration string like "30s" or "5m"
        """
        return self.sync(self._set_keepalive, keepalive)

    async def _set_keepalive(self, keepalive, retries=5):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.coiled_set_keepalive(keepalive=keepalive)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._set_keepalive(keepalive=keepalive, retries=retries - 1)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error setting keepalive on cluster: {e}")

    def _call_scheduler_comm(self, function: str, **kwargs):
        return self.sync(self._call_scheduler_comm_async, function, **kwargs)

    async def _call_scheduler_comm_async(self, function: str, retries=5, **kwargs):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await getattr(scheduler_comm, function)(**kwargs)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._call_scheduler_comm_async(function=function, retries=retries - 1, **kwargs)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error calling {function} on scheduler comm: {e}")

    def send_private_envs(self: ClusterSyncAsync, env: dict):
        """
        Send potentially private environment variables to be set on scheduler and all workers.

        You can use this to send secrets (passwords, auth tokens) that you can use in code running on cluster.
        Unlike environment variables set with ``coiled.Cluster(environ=...)``, the values will be transmitted
        directly to your cluster without being transmitted to Coiled, logged, or written to disk.

        The Dask scheduler will ensure that these environment variables are set on any new workers you add to the
        cluster.
        """
        return self.sync(self._send_env_vars, env)

    async def _send_env_vars(self, env: dict, retries=5):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.coiled_update_env_vars(env=env)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._send_env_vars(env, retries=retries - 1)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error sending environment variables to cluster: {e}")

    def unset_env_vars(self: ClusterSyncAsync, unset: list):
        return self.sync(self._unset_env_vars, unset)

    async def _unset_env_vars(self, unset: list, retries=5):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.coiled_unset_env_vars(unset=unset)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._unset_env_vars(unset, retries=retries - 1)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error unsetting environment variables on cluster: {e}")

    def send_credentials(self: ClusterSyncAsync, automatic_refresh: bool = False):
        """
        Manually trigger sending STS token to cluster.

        Usually STS token is automatically sent and refreshed by default, this allows
        you to manually force a refresh in case that's needed for any reason.
        """
        return self.sync(self._send_credentials, schedule_callback=automatic_refresh)

    def _schedule_cred_update(self, expiration: Optional[datetime.datetime], label: str, extra_warning: str = ""):
        # schedule callback for updating creds before they expire

        # default to updating every 45 minutes
        delay = 45 * 60

        if self._credentials_duration_seconds and self._credentials_duration_seconds < 900:
            # 15 minutes is min duration for STS token, but if shorter duration explicitly
            # requested, then we'll update as if that were the duration (with lower bound of 5s).
            delay = max(5, int(self._credentials_duration_seconds * 0.5))
        else:
            # Otherwise, get duration from expiration set on the STS token.
            if expiration:
                diff = expiration - datetime.datetime.now(tz=tz.UTC)
                delay = int((diff * 0.5).total_seconds())

                if diff < datetime.timedelta(minutes=5):
                    # usually the existing STS token will be from a role assumption and
                    # will expire in ~1 hour, but just in case the local session has a very
                    # short lived token, let the user know
                    # TODO give user information about what to do in this case
                    logger.warning(f"Locally generated {label} expires in less than 5 minutes ({diff}).{extra_warning}")

                # don't try to update sooner than in 1 minute
                delay = max(60, delay)
        if self.loop:
            # should never be None but distributed baseclass claims it can be
            self.loop.call_later(delay=delay, callback=self._send_credentials)
            logger.debug(f"{label} from local credentials shipped to cluster, planning to refresh in {delay} seconds")

    async def _send_aws_credentials(self, schedule_callback: bool):
        # AWS STS token
        token_creds = await self._get_aws_local_session_token(duration_seconds=self._credentials_duration_seconds)
        if token_creds and token_creds.get("SessionToken"):
            scheduler_comm = self._ensure_scheduler_comm()

            keys = [
                "AccessKeyId",
                "SecretAccessKey",
                "SessionToken",
                "DefaultRegion",
            ]

            # creds endpoint will be used iff expiration is sent to plugin
            # so this is a way to (for now) feature flag using creds endpoint (vs. env vars)
            if dask.config.get("coiled.use_aws_creds_endpoint", False):
                keys.append("Expiration")

            # values should be str | None; make sure we don't use "None"
            creds_to_send = {k: str(token_creds.get(k)) if token_creds.get(k) is not None else None for k in keys}
            await scheduler_comm.aws_update_credentials(credentials=creds_to_send)

            if schedule_callback:
                self._schedule_cred_update(
                    expiration=token_creds.get("Expiration"),
                    label="AWS STS token",
                    extra_warning=(
                        " Code running on your cluster may be unable to access other AWS services "
                        "(e.g, S3) when this token expires."
                    ),
                )
            else:
                logger.debug("AWS STS token from local credentials shipped to cluster, no scheduled refresh")
        elif dask.config.get("coiled.use_aws_creds_endpoint", False):
            # since we aren't shipping local creds, remove creds endpoint in credential chain
            await self._unset_env_vars(["AWS_CONTAINER_CREDENTIALS_FULL_URI"])

    async def _send_gcp_credentials(self, schedule_callback: bool):
        # Google Cloud OAuth2 token
        has_gcp_auth_installed = self._has_gcp_auth_installed()
        if self._try_local_gcp_creds and has_gcp_auth_installed:
            gcp_token = self._get_gcp_local_session_token()

            if gcp_token.get("token"):
                await self._send_env_vars({"CLOUDSDK_AUTH_ACCESS_TOKEN": gcp_token.get("token")})

                if gcp_token.get("expiry") and schedule_callback:
                    self._schedule_cred_update(expiration=gcp_token.get("expiry"), label="Google Cloud OAuth2 token")
                else:
                    logger.debug(
                        "Google Cloud OAuth2 token from local credentials shipped to cluster, no scheduled refresh"
                    )
            else:
                self._try_local_gcp_creds = False

    async def _send_credentials(self, schedule_callback: bool = True, retries=5):
        """
        Get credentials and pass them to the scheduler.
        """
        if self.credentials is CredentialsPreferred.NONE and dask.config.get("coiled.use_aws_creds_endpoint", False):
            await self._unset_env_vars(["AWS_CONTAINER_CREDENTIALS_FULL_URI"])

        if self.credentials is not CredentialsPreferred.NONE:
            try:
                if self.credentials is CredentialsPreferred.ACCOUNT:
                    # cloud.get_aws_credentials doesn't return credentials for currently implemented backends
                    # aws_creds = await cloud.get_aws_credentials(self.account)
                    logger.warning(
                        "Using account backend AWS credentials is not currently supported, "
                        "local AWS credentials (if present) will be used."
                    )

                # Concurrently handle AWS and GCP creds
                await asyncio.gather(
                    *[self._send_aws_credentials(schedule_callback), self._send_gcp_credentials(schedule_callback)]
                )

            except Exception as e:
                if self.status not in TERMINATING_STATES:
                    # sending credentials sometimes fails on a poor internet connection
                    # so try a few times before giving up and showing warning
                    if retries > 0:
                        await self._send_credentials(schedule_callback, retries=retries - 1)
                    else:
                        # no more retries!
                        # warn, but don't crash
                        logger.warning(f"error sending local AWS or Google Cloud credentials to cluster: {e}")

    def __await__(self: Cluster[Async]):
        async def _():
            if self._lock is None:
                self._lock = asyncio.Lock()
            async with self._lock:
                if self.status == Status.created:
                    await wait_for(self._start(), self.timeout)
                assert self.status == Status.running
            return self

        return _().__await__()

    @overload
    def close(self: Cluster[Sync], force_shutdown: bool = False) -> None:
        ...

    @overload
    def close(self: Cluster[Async], force_shutdown: bool = False) -> Awaitable[None]:
        ...

    def close(self: ClusterSyncAsync, force_shutdown: bool = False) -> Union[None, Awaitable[None]]:
        """
        Close the cluster.
        """
        return self.sync(self._close, force_shutdown=force_shutdown)

    @overload
    def shutdown(self: Cluster[Sync]) -> None:
        ...

    @overload
    def shutdown(self: Cluster[Async]) -> Awaitable[None]:
        ...

    def shutdown(self: ClusterSyncAsync) -> Union[None, Awaitable[None]]:
        """
        Shutdown the cluster; useful when shutdown_on_close is False.
        """
        return self.sync(self._close, force_shutdown=True)

    @overload
    def scale(self: Cluster[Sync], n: int) -> None:
        ...

    @overload
    def scale(self: Cluster[Async], n: int) -> Awaitable[None]:
        ...

    def scale(self: ClusterSyncAsync, n: int) -> Optional[Awaitable[None]]:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        n
            Number of workers to scale cluster size to.
        """
        return self.sync(self._scale, n=n)

    @track_context
    async def scale_down(self, workers: set, reason: Optional[str] = None) -> None:
        if not self.cluster_id:
            raise ValueError("No cluster available to scale!")
        cloud = cast(CloudV2[Async], self.cloud)
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.retire_workers(
                names=workers,
                remove=True,
                close_workers=True,
            )
        except Exception as e:
            logging.warning(f"error retiring workers {e}. Trying more forcefully")
        # close workers more forcefully
        await cloud._scale_down(
            account=self.account,
            cluster_id=self.cluster_id,
            workers=workers,
            reason=reason,
        )
        self._plan.difference_update(workers)
        self._requested.difference_update(workers)

    async def recommendations(self, target: int) -> dict:
        """
        Make scale up/down recommendations based on current state and target.

        Return a recommendation of the form
        - {"status": "same"}
        - {"status": "up", "n": <desired number of total workers>}
        - {"status": "down", "workers": <list of workers to close>}
        """
        # note that `Adaptive` has a `recommendations()` method, but (as far as I can tell) it doesn't
        # appear that adaptive ever calls `cluster.recommendations()`, so this appears to only be used
        # from `cluster.scale()`
        plan = self.plan
        requested = self.requested
        observed = self.observed

        n_current_or_expected = len(plan)

        if target == n_current_or_expected:
            return {"status": "same"}

        if target > n_current_or_expected:
            return {"status": "up", "n": target}

        # when scaling down, prefer workers that haven't yet connected to scheduler
        # for this to work, the worker name known by scheduler needs to match worker name in database
        not_yet_arrived = requested - observed
        to_close = set()
        if not_yet_arrived:
            to_close.update(islice(not_yet_arrived, n_current_or_expected - target))

        if target < n_current_or_expected - len(to_close):
            L = await self.workers_to_close(target=target)
            to_close.update(L)
        return {"status": "down", "workers": list(to_close)}

    async def _apply_scaling_recommendations(self, recommendations: dict):
        # structure of `recommendations` matches output of `self.recommendations()`
        status = recommendations.pop("status")
        if status == "same":
            return
        if status == "up":
            return await self.scale_up(**recommendations)
        if status == "down":
            return await self.scale_down(**recommendations)

    async def workers_to_close(self, target: int) -> List[str]:
        """
        Determine which, if any, workers should potentially be removed from
        the cluster.

        Notes
        -----
        ``Cluster.workers_to_close`` dispatches to Scheduler.workers_to_close(),
        but may be overridden in subclasses.

        Returns
        -------
        List of worker addresses to close, if any

        See Also
        --------
        Scheduler.workers_to_close
        """
        scheduler_comm = self._ensure_scheduler_comm()

        target_offset = 0
        if self.extra_worker_on_scheduler and target:
            # ask for an extra worker we can remove, so that if worker-on-scheduler is in the list
            # we can keep it alive and still get to target number of workers
            target_offset = 1
            target -= target_offset

        workers = await scheduler_comm.workers_to_close(
            target=target,
            attribute="name",
        )

        if self.extra_worker_on_scheduler and workers:
            # Never include the extra worker-on-scheduler in list of workers to kill.
            # Because we requested an extra possible worker (so we'd still get desired number if
            # worker-on-scheduler was in the list), we need only return the desired number (in case
            # extra worker-on-scheduler was *not* in the list of workers to kill).
            desired_workers = len(workers) - target_offset
            workers = list(filter(lambda name: "scheduler" not in name, workers))[:desired_workers]

        return workers  # type: ignore

    def adapt(
        self,
        Adaptive=CoiledAdaptive,
        *,
        minimum=1,
        maximum=200,
        target_duration="3m",
        wait_count=24,
        interval="5s",
        **kwargs,
    ) -> Adaptive:
        """Dynamically scale the number of workers in the cluster
        based on scaling heuristics.

        Parameters
        ----------
        minimum : int
            Minimum number of workers that the cluster should have while
            on low load, defaults to 1.
        maximum : int
            Maximum numbers of workers that the cluster should have while
            on high load.
        wait_count : int
            Number of consecutive times that a worker should be suggested
            for removal before the cluster removes it.
        interval : timedelta or str
            Milliseconds between checks, defaults to 5000 ms.
        target_duration : timedelta or str
            Amount of time we want a computation to take. This affects how
            aggressively the cluster scales up.

        """
        return super().adapt(
            Adaptive=Adaptive,
            minimum=minimum,
            maximum=maximum,
            target_duration=target_duration,
            wait_count=wait_count,
            interval=interval,
            **kwargs,
        )

    def __enter__(self: Cluster[Sync]) -> Cluster[Sync]:
        return self.sync(self.__aenter__)

    def __exit__(self: Cluster[Sync], *args, **kwargs) -> None:
        return self.sync(self.__aexit__, *args, **kwargs)

    @overload
    def get_logs(self: Cluster[Sync], scheduler: bool, workers: bool = True) -> dict:
        ...

    @overload
    def get_logs(self: Cluster[Async], scheduler: bool, workers: bool = True) -> Awaitable[dict]:
        ...

    def get_logs(self: ClusterSyncAsync, scheduler: bool = True, workers: bool = True) -> Union[dict, Awaitable[dict]]:
        """Return logs for the scheduler and workers
        Parameters
        ----------
        scheduler : boolean
            Whether or not to collect logs for the scheduler
        workers : boolean
            Whether or not to collect logs for the workers
        Returns
        -------
        logs: Dict[str]
            A dictionary of logs, with one item for the scheduler and one for
            the workers
        """
        return self.sync(self._get_logs, scheduler=scheduler, workers=workers)

    @track_context
    async def _get_logs(self, scheduler: bool = True, workers: bool = True) -> dict:
        if not self.cluster_id:
            raise ValueError("No cluster available for logs!")
        cloud = cast(CloudV2[Async], self.cloud)
        return await cloud.cluster_logs(
            cluster_id=self.cluster_id,
            account=self.account,
            scheduler=scheduler,
            workers=workers,
        )

    @overload
    def get_aggregated_metric(
        self: Cluster[Sync], query: str, over_time: str, start_ts: Optional[int] = None, end_ts: Optional[int] = None
    ) -> dict:
        ...

    @overload
    def get_aggregated_metric(
        self: Cluster[Async], query: str, over_time: str, start_ts: Optional[int] = None, end_ts: Optional[int] = None
    ) -> Awaitable[dict]:
        ...

    def get_aggregated_metric(
        self: ClusterSyncAsync, query: str, over_time: str, start_ts: Optional[int] = None, end_ts: Optional[int] = None
    ) -> Union[dict, Awaitable[dict]]:
        return self.sync(
            self._get_aggregated_metric, query=query, over_time=over_time, start_ts=start_ts, end_ts=end_ts
        )

    @track_context
    async def _get_aggregated_metric(
        self, query: str, over_time: str, start_ts: Optional[int] = None, end_ts: Optional[int] = None
    ) -> dict:
        if not self.cluster_id:
            raise ValueError("No cluster available for metrics!")
        cloud = cast(CloudV2[Async], self.cloud)
        return await cloud._get_cluster_aggregated_metric(
            cluster_id=self.cluster_id,
            account=self.account,
            query=query,
            over_time=over_time,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    @overload
    def add_span(self: Cluster[Sync], span_identifier: str, data: dict):
        ...

    @overload
    def add_span(self: Cluster[Async], span_identifier: str, data: dict):
        ...

    def add_span(self: ClusterSyncAsync, span_identifier: str, data: dict):
        self.sync(
            self._add_span,
            span_identifier=span_identifier,
            data=data,
        )

    @track_context
    async def _add_span(self, span_identifier: str, data: dict):
        if not self.cluster_id:
            raise ValueError("No cluster available")
        cloud = cast(CloudV2[Async], self.cloud)
        await cloud._add_cluster_span(
            cluster_id=self.cluster_id,
            account=self.account,
            span_identifier=span_identifier,
            data=data,
        )

    @property
    def dashboard_link(self):
        if EXECUTION_CONTEXT == "notebook":
            # dask-labextension has trouble following the token in query, so we'll give it the token
            # in the url path, which our dashboard auth also accepts.
            parsed = parse_url(self._dashboard_address)
            if parsed.query and parsed.query.startswith("token="):
                token = parsed.query[6:]
                path_with_token = f"/{token}/status" if not parsed.path else f"/{token}{parsed.path}"
                return parsed._replace(path=path_with_token)._replace(query=None).url

        return self._dashboard_address

    @property
    def jupyter_link(self):
        if not self.scheduler_options.get("jupyter"):
            logger.warning(
                "Jupyter was not enabled on the cluster scheduler. "
                "Use `scheduler_options={'jupyter': True}` to enable."
            )
        return parse_url(self._dashboard_address)._replace(path="/jupyter/lab").url


def __getattr__(name):
    if name == "ClusterBeta":
        warnings.warn(
            "`ClusterBeta` is deprecated and will be removed in a future release. Use `Cluster` instead.",
            category=FutureWarning,
            stacklevel=2,
        )
        return Cluster
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")
