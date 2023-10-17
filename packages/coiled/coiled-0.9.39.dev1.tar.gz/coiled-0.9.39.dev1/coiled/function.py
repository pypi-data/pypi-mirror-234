from __future__ import annotations

import os
import sys
import threading
import warnings
from collections.abc import Iterator
from typing import Optional, Union

import dask.distributed
import toolz
from dask.base import tokenize
from dask.utils import parse_timedelta

import coiled

_clients = {}
_lock = threading.RLock()
_clusters = {}


class Function:
    """A function that you can run remotely"""

    def __init__(self, function, cluster_kwargs, keepalive):
        self.function = function
        self._cluster_kwargs = cluster_kwargs
        self.keepalive = parse_timedelta(keepalive)

        token = tokenize(
            sys.executable,
            # TODO: include something about the software environment
            **cluster_kwargs,
        )
        self._name = f"function-{token[:8]}"

    @property
    def cluster(self) -> coiled.Cluster:
        with _lock:
            try:
                return _clusters[self._name]
            except KeyError:
                cluster = coiled.Cluster(name=self._name, **self._cluster_kwargs)
                cluster.adapt(minimum=0, maximum=500)
                _clusters[self._name] = cluster
                return cluster

    @property
    def client(self) -> dask.distributed.Client:
        with _lock:
            try:
                return _clients[self._name]
            except KeyError:
                client = dask.distributed.Client(self.cluster, set_as_default=False)
                if self.cluster.shutdown_on_close:
                    self.cluster.set_keepalive(keepalive=self.keepalive)
                _clients[self._name] = client
                return client

    def __call__(self, *args, **kwargs):
        # If this is being called from on the desired cluster, then run locally.
        # This allows one Function (with same desired cluster specs) to call another without overhead.
        if os.environ.get("COILED_CLUSTER_NAME", None) == self._name:
            return self.local(*args, **kwargs)
        # Otherwise, submit to cluster.
        return self.submit(*args, **kwargs).result()

    def local(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def submit(self, *args, **kwargs) -> dask.distributed.Future:
        """Submit function call for asynchronous execution

        This immediately returns a Dask Future, allowing for the submission of
        many tasks in parallel.

        Example
        -------
        >>> @coiled.function()
        ... def f(x):
        ...    return x + 1

        >>> f(10)  # calling the function blocks until finished
        11
        >>> f.submit(10)  # immediately returns a future
        <Future: pending, key=f-1234>
        >>> f.submit(10).result()  # Call .result to get result
        11

        >>> futures = [f(i) for i in range(1000)]  # parallelize with a for loop
        >>> [future.result() for future in futures]
        ...

        Returns
        -------
        future: dask.distributed.Future

        See Also
        --------
        Function.map
        """
        return self.client.submit(self.function, *args, **kwargs)

    def map(self, *args, **kwargs) -> Iterator:
        """Map function across many inputs

        This runs your function many times in parallel across all of the items
        in an input list.  Coiled will auto-scale your cluster to meet demand.

        Example
        -------
        >>> @coiled.function()
        ... def process(filename: str):
        ...     " Convert CSV file to Parquet "
        ...     df = pd.read_csv(filename)
        ...     outfile = filename[:-4] + ".parquet"
        ...     df.to_parquet(outfile)
        ...     return outfile

        >>> process("s3://my-bucket/data.csv")  # calling the function blocks until finished
        11
        >>> filenames = process.map(filenames)
        >>> print(list(filenames))  # print out all output filenames

        Returns
        -------
        results: Iterator

        See Also
        --------
        Function.submit
        """
        kwargs.setdefault("pure", False)
        kwargs.setdefault("batch_size", 100)
        futures = self.client.map(self.function, *args, **kwargs)
        batchsize = max(int(len(futures) / 50), 1)  # type: ignore
        batches = toolz.partition_all(batchsize, futures)
        return (result for batch in batches for result in self.client.gather(batch))  # type: ignore


def function(
    *,
    software: Optional[str] = None,
    container: Optional[str] = None,
    vm_type: Optional[Union[str, list[str]]] = None,
    cpu: Optional[Union[int, list[int]]] = None,
    memory: Optional[Union[str, list[str]]] = None,
    gpu: Optional[bool] = None,
    account: Optional[str] = None,
    region: Optional[str] = None,
    arm: Optional[bool] = None,
    disk_size: Optional[int] = None,
    shutdown_on_close: bool = True,
    spot_policy: Optional[str] = None,
    idle_timeout: str = "24 hours",
    keepalive="30 seconds",
    threads_per_worker: Union[int, None] = 1,
):
    """
    Decorate a function to run on cloud infrastructure

    This creates a ``Function`` object that executes its code on a remote cluster
    with the hardware and software specified in the arguments to the decorator.
    It can run either as a normal function, or it can return Dask Futures for
    parallel computing.

    Parameters
    ----------
    software
        Name of the software environment to use; this allows you to use and re-use existing
        Coiled software environments, and should not be used with package sync or when specifying
        a container to use for this specific cluster.
    container
        Name or URI of container image to use; when using a pre-made container image with Coiled,
        this allows you to skip the step of explicitly creating a Coiled software environment
        from that image. Note that this should not be used with package sync or when specifying
        an existing Coiled software environment.
    vm_type
        Instance type, or list of instance types, that you would like to use.
        You can use ``coiled.list_instance_types()`` to see a list of allowed types.
    cpu
        Number, or range, of CPUs requested. Specify a range by
        using a list of two elements, for example: ``cpu=[2, 8]``.
    memory
        Amount of memory to request for each VM, Coiled will use a +/- 10% buffer
        from the memory that you specify. You may specify a range of memory by using a
        list of two elements, for example: ``memory=["2GiB", "4GiB"]``.
    disk_size
        Size of persistent disk attached to each VM instance, specified in GiB.
    gpu
        Whether to attach a GPU; this would be a single NVIDIA T4.
    region
        The cloud provider region in which to run the cluster.
    arm
        Whether to use ARM instances for cluster; default is x86 (Intel) instances.
    keepalive
        Keep your cluster running for the specified time, even if your Python session closes.
        Default is "30 seconds".
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
    idle_timeout
        Shut down the cluster after this duration if no activity has occurred. Default is "24 hours".
    threads_per_worker
        Number of threads to run concurrent tasks in for each VM. -1 can be used to run as many concurrent
        tasks as there are CPU cores. Default is 1.


    See the :class:`coiled.Cluster` docstring for additional parameter descriptions.

    Examples
    --------
    >>> import coiled
    >>> @coiled.function()
    ... def f(x):
    ...    return x + 1

    >>> f(10)  # calling the function blocks until finished
    11
    >>> f.submit(10)  # immediately returns a future
    <Future: pending, key=f-1234>
    >>> f.submit(10).result()  # Call .result to get result
    11

    >>> futures = [f(i) for i in range(1000)]  # parallelize with a for loop
    >>> [future.result() for future in futures]
    ...
    """

    def decorator(func) -> Function:
        nonlocal cpu, threads_per_worker

        environ = coiled.utils.unset_single_thread_defaults()
        if container and "rapidsai" in container:
            environ = {"DISABLE_JUPYTER": "true", **environ}  # needed for "stable" RAPIDS image

        if memory is None and cpu is None and not vm_type:
            cpu = 2

        if threads_per_worker == -1:
            # Have `-1` mean the same as CPU count (Dask's default behavior)
            threads_per_worker = None

        cluster_kwargs = dict(
            account=account,
            n_workers=0,
            scheduler_cpu=cpu,
            scheduler_memory=memory,
            worker_cpu=cpu,
            worker_memory=memory,
            software=software,
            container=container,
            idle_timeout=idle_timeout,
            scheduler_vm_types=vm_type,
            worker_vm_types=vm_type,
            allow_ssh=True,
            environ=environ,
            scheduler_gpu=gpu,
            region=region,
            arm=arm,
            shutdown_on_close=shutdown_on_close,
            spot_policy=spot_policy,
            extra_worker_on_scheduler=True,
            tags={"coiled-cluster-type": "function"},
            worker_options={"nthreads": threads_per_worker},
            scheduler_disk_size=disk_size,
            worker_disk_size=disk_size,
        )

        return Function(func, cluster_kwargs, keepalive=keepalive)

    return decorator


# Small backwards compatibility shim
def run(*args, **kwargs):
    warnings.warn(
        "coiled.run has been renamed to coiled.function. "
        "Please use coiled.function as coiled.run will be removed in a future release.",
        FutureWarning,
        stacklevel=2,
    )
    return function(*args, **kwargs)
