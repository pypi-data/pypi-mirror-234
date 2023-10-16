import asyncio
import logging
import platform
import re
import shutil
import subprocess
import sys
import typing
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from sys import executable
from tempfile import TemporaryDirectory
from threading import Lock
from typing import Dict, List, Optional, Set, TextIO, Tuple, Union, cast
from urllib.parse import urlparse

from dask import config
from filelock import BaseFileLock, FileLock
from packaging.utils import parse_wheel_filename
from rich.progress import Progress
from typing_extensions import Literal

from coiled.context import track_context
from coiled.scan import PackageInfo, scan_prefix
from coiled.types import ArchitectureTypesEnum, PackageLevelEnum, ResolvedPackageInfo
from coiled.utils import COILED_LOCAL_PACKAGE_PREFIX, recurse_importable_python_files, validate_wheel
from coiled.v2.core import CloudV2
from coiled.v2.widgets.util import simple_progress

logger = getLogger("coiled.package_sync")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()
ANY_AVAILABLE = "ANY-AVAILABLE"


async def create_subprocess_shell(
    cmd: str,
    stdout: Union[TextIO, int, None] = None,
    stderr: Union[TextIO, int, None] = None,
) -> subprocess.CompletedProcess:
    # asyncio.create_subprocess_shell is
    # not supported on windows
    # and broken on py3.7
    loop = asyncio.get_running_loop()
    result = loop.run_in_executor(
        None, lambda: subprocess.run(cmd, shell=True, stdout=stdout, stderr=stderr, close_fds=True)
    )
    return await result


class PackageBuildError(Exception):
    pass


WHEEL_BUILD_LOCKS: Dict[str, Tuple[BaseFileLock, Lock, TemporaryDirectory]] = {}


async def default_python() -> PackageInfo:
    python_version = platform.python_version()
    return {
        "name": "python",
        "path": None,
        "source": "conda",
        "channel_url": ANY_AVAILABLE,
        "channel": ANY_AVAILABLE,
        "subdir": "linux-64",
        "conda_name": "python",
        "version": python_version,
        "wheel_target": None,
    }


# filelock is thread local
# so we have to ensure the lock is acquired/released
# on the same thread
FILE_LOCK_POOL = ThreadPoolExecutor(max_workers=1)
THREAD_LOCK_POOL = ThreadPoolExecutor(max_workers=1)


@asynccontextmanager
async def async_lock(file_lock: BaseFileLock, thread_lock: Lock):
    # Beware, there are some complicated details to this locking implementation!
    # We're trying to manage the weirdness of the file lock mostly.
    loop = asyncio.get_event_loop()
    # first acquire a thread lock
    await loop.run_in_executor(THREAD_LOCK_POOL, thread_lock.acquire)
    # acquire the file lock, we should be the only thread trying to get it
    # the threadpool is required to release it, so another thread
    # attempting to get the lock will deadlock things by preventing the
    # release!
    await loop.run_in_executor(FILE_LOCK_POOL, file_lock.acquire)
    yield
    # release the file lock first
    await loop.run_in_executor(FILE_LOCK_POOL, file_lock.release)
    # now release the thread lock, allowing another thread to proceed
    # and get the file lock
    thread_lock.release()


@track_context
async def create_wheel(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    # These locks are set up such that
    # Threads: Block on each other and check if another thread already built the wheel
    # Processes: Block on each other, but will not reuse a wheel created by another
    # `pip wheel` is never run on the same package at the same time
    lock_path = Path(config.PATH)
    lock_path.mkdir(parents=True, exist_ok=True)  # ensure lockfile directory exists
    package_lock, thread_lock, tmpdir = WHEEL_BUILD_LOCKS.setdefault(
        pkg_name,
        (FileLock(lock_path / ("." + pkg_name + version + ".build-lock")), Lock(), TemporaryDirectory()),
    )
    async with async_lock(package_lock, thread_lock):
        outdir = Path(tmpdir.name) / Path(pkg_name)
        if outdir.exists():
            logger.debug(f"Checking for existing wheel for {pkg_name} @ {outdir}")
            wheel_fn = next((file for file in outdir.iterdir() if file.suffix == ".whl"), None)
        else:
            wheel_fn = None
        if not wheel_fn:
            logger.debug(f"No existing wheel, creating a wheel for {pkg_name} @ {src}")
            # must use executable to avoid using some other random python
            p = await create_subprocess_shell(
                cmd=f"{executable} -m pip wheel --wheel-dir {outdir} --no-deps --use-pep517 --no-cache-dir {src}",
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
            )
            if p.returncode:
                print(
                    f"---Wheel Build Log for {pkg_name}---\n" + p.stdout.decode(encoding=sys.stdout.encoding or "utf-8")
                )
                return {
                    "name": pkg_name,
                    "source": "pip",
                    "channel": None,
                    "conda_name": None,
                    "client_version": version,
                    "specifier": "",
                    "include": False,
                    "error": (
                        "Failed to build a wheel for the"
                        " package, will not be included in environment, check stdout for the build log"
                    ),
                    "note": None,
                    "sdist": None,
                    "md5": None,
                }
            wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
        logger.debug(f"Using wheel @ {wheel_fn}")
        _, build_version, _, _ = parse_wheel_filename(str(wheel_fn.name))
        has_python, md5, missing_py_files = await validate_wheel(wheel_fn, src)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": str(build_version),
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel contains no python files!",
        "note": (
            f"Wheel built from {src}"
            + (f" is missing {', '.join(sorted(missing_py_files)[:10])}" if missing_py_files else "")
        ),
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


@track_context
async def create_wheel_from_egg(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    tmpdir = TemporaryDirectory()
    outdir = Path(tmpdir.name) / Path(pkg_name)
    outdir.mkdir(parents=True)
    logger.debug(f"Attempting to create a wheel for {pkg_name} in directory {src}")
    # must use executable to avoid using some other random python
    p = await create_subprocess_shell(
        cmd=f"{executable} -m wheel convert --dest-dir {outdir} {src}",
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if p.returncode:
        print(
            f"---Egg to wheel conversion Log for {pkg_name}---\n"
            + p.stdout.decode(encoding=sys.stdout.encoding or "utf-8")
        )
        return {
            "name": pkg_name,
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": version,
            "specifier": "",
            "include": False,
            "error": (
                "Failed to convert the package egg to a wheel"
                ", will not be included in environment, check stdout for egg conversion log"
            ),
            "note": None,
            "sdist": None,
            "md5": None,
        }
    wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
    has_python, md5, missing_py_files = await validate_wheel(Path(wheel_fn), tmpdir.name)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": version,
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel has no python files!",
        "note": (
            "Wheel built from local egg"
            + (f" is missing {', '.join(sorted(missing_py_files)[:10])}" if missing_py_files else "")
        ),
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


@track_context
async def create_wheel_from_src_dir(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    # These locks are set up such that
    # Threads: Block on each other and check if another thread already built the tarball
    # Processes: Block on each other, but will not reuse a tarball created by another
    md5 = None
    lock_path = Path(config.PATH)
    lock_path.mkdir(parents=True, exist_ok=True)  # ensure lockfile directory exists
    package_lock, thread_lock, tmpdir = WHEEL_BUILD_LOCKS.setdefault(
        pkg_name,
        (FileLock(lock_path / (f".{pkg_name}{version}.build-lock")), Lock(), TemporaryDirectory()),
    )
    async with async_lock(package_lock, thread_lock):
        outdir = Path(tmpdir.name) / Path(pkg_name)
        if outdir.exists():
            logger.debug(f"Checking for existing source archive for {pkg_name} @ {outdir}")
            wheel_fn = next((file for file in outdir.iterdir() if file.suffix == ".whl"), None)
        else:
            wheel_fn = None
        if not wheel_fn:
            logger.debug(f"No existing source archive, creating an archive for {pkg_name} @ {src}")
            try:
                unpacked_dir = outdir / f"{pkg_name}-{version}"
                # Create fake metadata to make wheel work
                dist_info_dir = unpacked_dir / f"{unpacked_dir.name}.dist-info"
                dist_info_dir.mkdir(parents=True)
                with open(dist_info_dir / "METADATA", "w") as f:
                    f.write(f"Metadata-Version: 2.1\nName: {pkg_name}\nVersion: {version}\n")
                with open(dist_info_dir / "WHEEL", "w") as f:
                    f.write("Wheel-Version: 1.0\nGenerator: coiled\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
                src_path = Path(src)
                for file in recurse_importable_python_files(src_path):
                    if str(file) in ("__init__.py", "__main__.py"):
                        continue
                    dest = unpacked_dir / file
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(src_path / file, dest)
                p = await create_subprocess_shell(
                    cmd=f"{executable} -m wheel pack --dest-dir {outdir} {unpacked_dir}",
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE,
                )
                if p.returncode:
                    print(
                        f"---wheel packing log for {src}---\n"
                        + p.stdout.decode(encoding=sys.stdout.encoding or "utf-8")
                    )
                    return {
                        "name": pkg_name,
                        "source": "pip",
                        "channel": None,
                        "conda_name": None,
                        "client_version": version,
                        "specifier": "",
                        "include": False,
                        "error": (
                            "Failed to build a package of your local python files. Please check stdout for details"
                        ),
                        "note": None,
                        "sdist": None,
                        "md5": None,
                    }
            except IOError as e:
                return {
                    "name": pkg_name,
                    "source": "pip",
                    "channel": None,
                    "conda_name": None,
                    "client_version": version,
                    "specifier": "",
                    "include": False,
                    "error": f"Failed to build a package of your local python files. Exception: {e}",
                    "note": None,
                    "sdist": None,
                    "md5": None,
                }
            wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
        logger.debug(f"Using wheel @ {wheel_fn}")
        _, build_version, _, _ = parse_wheel_filename(str(wheel_fn.name))
        has_python, md5, missing_py_files = await validate_wheel(wheel_fn, src)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": str(build_version),
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel does not contain all python files!",
        "note": (
            f"Source wheel built from {src}"
            + (f" is missing {', '.join(sorted(missing_py_files)[:10])}" if missing_py_files else "")
        ),
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


@track_context
async def approximate_packages(
    cloud: CloudV2,
    packages: List[PackageInfo],
    priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum],
    progress: Optional[Progress] = None,
    strict: bool = False,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
) -> typing.List[ResolvedPackageInfo]:
    user_conda_installed_python = next((p for p in packages if p["name"] == "python"), None)
    user_conda_installed_pip = next(
        (i for i, p in enumerate(packages) if p["name"] == "pip" and p["source"] == "conda"),
        None,
    )
    if not user_conda_installed_pip:
        # This means pip was installed by pip, or the system
        # package manager
        # Insert a conda version of pip to be installed first, it will
        # then be used to install the users version of pip
        pip = next(
            (p for p in packages if p["name"] == "pip" and p["source"] == "pip"),
            None,
        )
        if not pip:
            # insert a modern version and hope it does not introduce conflicts
            packages.append(
                {
                    "name": "pip",
                    "path": None,
                    "source": "conda",
                    "channel_url": "https://conda.anaconda.org/conda-forge/",
                    "channel": "conda-forge",
                    "subdir": "noarch",
                    "conda_name": "pip",
                    "version": "22.3.1",
                    "wheel_target": None,
                }
            )
        else:
            # insert the users pip version and hope it exists on conda-forge
            packages.append(
                {
                    "name": "pip",
                    "path": None,
                    "source": "conda",
                    "channel_url": "https://conda.anaconda.org/conda-forge/",
                    "channel": "conda-forge",
                    "subdir": "noarch",
                    "conda_name": "pip",
                    "version": pip["version"],
                    "wheel_target": None,
                }
            )
    coiled_selected_python = None
    if not user_conda_installed_python:
        # insert a special python package
        # that the backend will pick a channel for
        coiled_selected_python = await default_python()
        packages.append(coiled_selected_python)

    local_packages: List[PackageInfo] = [pkg for pkg in packages if pkg["name"].startswith(COILED_LOCAL_PACKAGE_PREFIX)]
    packages = [pkg for pkg in packages if not pkg["name"].startswith(COILED_LOCAL_PACKAGE_PREFIX)]

    with simple_progress("Validating environment", progress=progress):
        results = await cloud._approximate_packages(
            packages=[
                {
                    "name": pkg["name"],
                    "priority_override": (
                        PackageLevelEnum.CRITICAL
                        if (
                            strict
                            or (
                                pkg["wheel_target"]
                                # Ignore should override wheel_target (see #2640)
                                and not priorities.get((pkg["name"], pkg["source"])) == PackageLevelEnum.IGNORE
                            )
                        )
                        else priorities.get(
                            ((cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]), pkg["source"])
                        )
                    ),
                    "python_major_version": PYTHON_VERSION[0],
                    "python_minor_version": PYTHON_VERSION[1],
                    "python_patch_version": PYTHON_VERSION[2],
                    "source": pkg["source"],
                    "channel_url": pkg["channel_url"],
                    "channel": pkg["channel"],
                    "subdir": pkg["subdir"],
                    "conda_name": pkg["conda_name"],
                    "version": pkg["version"],
                    "wheel_target": pkg["wheel_target"],
                }
                for pkg in packages
            ],
            architecture=architecture,
        )
    result_map = {(r["name"], r["conda_name"]): r for r in results}
    finalized_packages: typing.List[ResolvedPackageInfo] = []

    if not user_conda_installed_python and coiled_selected_python:
        # user has no python version installed by conda
        # we should have a result of asking the backend to
        # pick conda channel that has the users python version
        python_result = result_map[("python", "python")]
        if result_map[("python", "python")]["error"]:
            finalized_packages.append(
                {
                    "name": "python",
                    "source": "conda",
                    "channel": None,
                    "conda_name": "python",
                    "client_version": coiled_selected_python["version"],
                    "specifier": python_result["specifier"] or "",
                    "include": python_result["include"],
                    "note": None,
                    "error": python_result["error"],
                    "sdist": None,
                    "md5": None,
                }
            )
        else:
            note = python_result["note"]
            if not note:
                raise ValueError("Expected a note from the backend")
            channel_url, channel = note.split(",")
            finalized_packages.append(
                {
                    "name": "python",
                    "source": "conda",
                    "channel": channel,
                    "conda_name": "python",
                    "client_version": coiled_selected_python["version"],
                    "specifier": python_result["specifier"] or "",
                    "include": python_result["include"],
                    "note": None,
                    "error": python_result["error"],
                    "sdist": None,
                    "md5": None,
                }
            )
        # we can pull our special python package out of the list
        # now
        packages.remove(coiled_selected_python)
    for pkg in local_packages:
        if pkg["wheel_target"]:
            with simple_progress(f'Creating wheel for {pkg["wheel_target"]}', progress=progress):
                finalized_packages.append(
                    await create_wheel_from_src_dir(
                        pkg_name=pkg["name"],
                        version=pkg["version"],
                        src=pkg["wheel_target"],
                    )
                )
    for pkg in packages:
        package_result = result_map[(pkg["name"], pkg["conda_name"])]
        if pkg["wheel_target"] and package_result["include"]:
            p = urlparse(pkg["wheel_target"])
            if len(p.scheme) <= 1 and not Path(pkg["wheel_target"]).exists():
                # lack of scheme (or it being a 1-char drive letter) means a local file
                # sometimes the wheel target taken from
                # direct_url.json references a file that does not exist
                # skip over trying to sync that and treat it like a normal package
                # this can happen in conda/system packages
                # where the package metadata was generated on a build system and not locally
                finalized_packages.append(
                    {
                        "name": pkg["name"],
                        "source": pkg["source"],
                        "channel": pkg["channel"],
                        "conda_name": pkg["conda_name"],
                        "client_version": pkg["version"],
                        "specifier": package_result["specifier"] or "",
                        "include": package_result["include"],
                        "note": package_result["note"],
                        "error": package_result["error"],
                        "sdist": None,
                        "md5": None,
                    }
                )
            elif pkg["wheel_target"].endswith(".egg"):
                with simple_progress(f'Creating wheel from egg for {pkg["name"]}', progress=progress):
                    finalized_packages.append(
                        await create_wheel_from_egg(
                            pkg_name=pkg["name"],
                            version=pkg["version"],
                            src=pkg["wheel_target"],
                        )
                    )
            else:
                with simple_progress(f'Creating wheel for {pkg["name"]}', progress=progress):
                    finalized_packages.append(
                        await create_wheel(
                            pkg_name=pkg["name"],
                            version=pkg["version"],
                            src=pkg["wheel_target"],
                        )
                    )
        else:
            finalized_packages.append(
                {
                    "name": pkg["name"],
                    "source": pkg["source"],
                    "channel": pkg["channel"],
                    "conda_name": pkg["conda_name"],
                    "client_version": pkg["version"],
                    "specifier": package_result["specifier"] or "",
                    "include": package_result["include"],
                    "note": package_result["note"],
                    "error": package_result["error"],
                    "sdist": None,
                    "md5": None,
                }
            )
    return finalized_packages


pip_bad_req_regex = (
    r"(?P<package>.+) (?P<version>.+) has requirement "
    r"(?P<requirement>.+), but you have (?P<requirement2>.+) (?P<reqversion>.+)."
)


@track_context
async def check_pip_happy(progress: Optional[Progress] = None) -> Dict[str, List[str]]:
    with simple_progress("Running pip check", progress=progress):
        proc = await create_subprocess_shell(
            f"{executable} -m pip check", stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        faulty_packages = defaultdict(list)
        if proc.returncode:
            output = proc.stdout.decode(encoding=sys.stdout.encoding or "utf-8")
            bad_reqs = re.finditer(pip_bad_req_regex, output)
            for bad_req in bad_reqs:
                groups = bad_req.groupdict()
                span = bad_req.span()
                warning = output[span[0] : span[1]]
                logger.warning(warning)
                faulty_packages[groups["package"]].append(warning)
        return faulty_packages


@track_context
async def create_environment_approximation(
    cloud: CloudV2,
    priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum],
    only: Optional[Set[str]] = None,
    strict: bool = False,
    progress: Optional[Progress] = None,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
) -> typing.List[ResolvedPackageInfo]:
    packages = await scan_prefix(progress=progress)
    bad_packages = await check_pip_happy(progress)
    if bad_packages:
        packages = [pkg for pkg in packages if pkg["name"] not in bad_packages]
    if only:
        packages = filter(lambda pkg: pkg["name"] in only, packages)
    # TODO: private conda channels
    result = await approximate_packages(
        cloud=cloud,
        packages=[pkg for pkg in packages],
        priorities=priorities,
        strict=strict,
        progress=progress,
        architecture=architecture,
    )
    for bad_package, error_list in bad_packages.items():
        errors = "\n".join(error_list)
        result.append(
            {
                "name": bad_package,
                "error": f"Pip check had the following issues that need resolving: \n{errors}",
                "source": "pip",
                "channel": None,
                "client_version": "",
                "conda_name": None,
                "include": False,
                "md5": None,
                "note": None,
                "sdist": None,
                "specifier": "",
            }
        )
    return result


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)

    from rich.console import Console
    from rich.table import Table

    async def run():
        async with CloudV2(asynchronous=True) as cloud:
            return await create_environment_approximation(
                cloud=cloud,
                priorities={
                    ("dask", "conda"): PackageLevelEnum.CRITICAL,
                    ("twisted", "conda"): PackageLevelEnum.IGNORE,
                    ("graphviz", "conda"): PackageLevelEnum.LOOSE,
                    ("icu", "conda"): PackageLevelEnum.LOOSE,
                },
            )

    result = asyncio.run(run())

    table = Table(title="Packages")
    keys = ("name", "source", "include", "client_version", "specifier", "error", "note")

    for key in keys:
        table.add_column(key)

    for pkg in result:
        row_values = [str(pkg.get(key, "")) for key in keys]
        table.add_row(*row_values)
    console = Console()
    console.print(table)
    console.print(table)
