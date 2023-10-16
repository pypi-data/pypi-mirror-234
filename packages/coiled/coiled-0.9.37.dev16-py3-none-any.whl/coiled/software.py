import pathlib
import platform
from logging import getLogger
from pathlib import Path
from typing import List, Union

from yaml import safe_load

from coiled.types import CondaEnvSchema, PackageSchema, SoftwareEnvSpec

logger = getLogger(__file__)


async def default_python() -> PackageSchema:
    python_version = platform.python_version()
    return {
        "name": "python",
        "source": "conda",
        "channel": "pkgs/main",
        "conda_name": "python",
        "client_version": python_version,
        "include": True,
        "specifier": f"=={python_version}",
        "file": None,
    }


def parse_env_yaml(env_path: Path) -> CondaEnvSchema:
    try:
        with env_path.open("rt") as env_file:
            conda_data = safe_load(env_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Unable to find file '{env_path}', please make sure it exists "
            "and the path is correct. If you are trying to create a "
            "software environment by specifying dependencies, you can "
            "do so by passing a list of dependencies or a dictionary. For example:\n"
            "\tcoiled.create_software_environment(\n"
            "\t    name='my-env', conda={'channels': ['conda-forge'], 'dependencies': ['coiled']}\n"
            "\t)"
        )
    return {
        "channels": conda_data["channels"],
        "dependencies": conda_data["dependencies"],
    }


def parse_conda(conda: Union[CondaEnvSchema, str, pathlib.Path, list]) -> CondaEnvSchema:
    if isinstance(conda, (str, pathlib.Path)):
        logger.info(f"Attempting to load environment file {conda}")
        schema = parse_env_yaml(Path(conda))
    elif isinstance(conda, list):
        schema = {"dependencies": conda}
    else:
        schema = conda
    if "channels" not in schema:
        schema["channels"] = ["conda-forge"]
    if "dependencies" not in schema:
        raise TypeError("No dependencies in conda spec")
    return {
        "channels": schema["channels"],
        "dependencies": schema["dependencies"],
    }


def parse_pip(pip: Union[List[str], str, Path]) -> List[str]:
    if isinstance(pip, (str, Path)):
        try:
            reqs = Path(pip).read_text().splitlines()
            return reqs
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Unable to find file '{pip}', please make sure it exists "
                "and the path is correct. If you are trying to create a "
                "software environment by specifying dependencies, you can "
                "do so by passing a list of dependencies. For example:\n"
                "\tcoiled.create_software_environment(\n"
                "\t    name='my-env', pip=['coiled']\n"
                "\t)"
            )
    else:
        return pip


async def create_env_spec(
    conda: Union[CondaEnvSchema, str, Path, list, None] = None,
    pip: Union[List[str], str, Path, None] = None,
) -> SoftwareEnvSpec:
    if not conda and not pip:
        raise TypeError("Either or both of conda/pip kwargs must be specified")
    spec: SoftwareEnvSpec = {"packages": [], "raw_conda": None, "raw_pip": None}
    if conda:
        spec["raw_conda"] = parse_conda(conda)
    if not conda:
        spec["packages"].append(await default_python())
    if pip:
        spec["raw_pip"] = parse_pip(pip)
    conda_installed_pip = any(p for p in spec["packages"] if p["name"] == "pip" and p["source"] == "conda")
    has_pip_installed_package = any(p for p in spec["packages"] if p["source"] == "pip")
    if not conda_installed_pip and has_pip_installed_package:
        spec["packages"].append(
            {
                "name": "pip",
                "source": "conda",
                "channel": "pkgs/main",
                "conda_name": "pip",
                "client_version": None,
                "include": True,
                "specifier": "",
                "file": None,
            }
        )
    return spec
