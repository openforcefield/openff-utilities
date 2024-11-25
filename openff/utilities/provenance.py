import functools
import subprocess
import warnings
from typing import Optional


@functools.lru_cache
def _get_conda_list_package_versions() -> dict[str, str]:
    """
    Returns the versions of any packages found while executing `conda list`.
    If no conda executable is found, emits CondaExecutableNotFoundWarning
    """
    from openff.utilities.utilities import has_executable
    from openff.utilities.warnings import CondaExecutableNotFoundWarning

    if has_executable("micromamba"):
        conda_executable = "micromamba"
    elif has_executable("mamba"):
        conda_executable = "mamba"
    elif has_executable("pixi"):
        conda_executable = "pixi"
    elif has_executable("conda"):
        conda_executable = "conda"
    else:
        warnings.warn(
            "No conda/mamba/micromamba executable found. Unable to determine package versions.",
            CondaExecutableNotFoundWarning,
        )
        return dict()

    output = list(
        filter(
            lambda x: len(x) > 0,
            subprocess.check_output([conda_executable, "list"]).decode().split("\n"),
        )
    )

    package_versions = {}

    for output_line in output[3:-1]:
        # The output format of `conda`/`mamba list` and `micromamba list` are different.
        # See https://github.com/openforcefield/openff-utilities/issues/65
        package_name, package_version, *_ = output_line.split()
        package_versions[package_name] = package_version

    return package_versions


def get_ambertools_version() -> Optional[str]:
    """
    Attempts to retrieve the version of the currently installed AmberTools.

    There are two soft failure modes, each of which cause this function to return `None`:
        1. If there is a failure calling `{conda|mamba|etc.} list`, the user is
            warned by `_get_conda_list_package_versions` and this function returns `None`.
        2. If there is a failure calling `{conda|mamba|etc.} list`, this function
            still returns `None`, but without a warning associated with the above failure.
    """

    return _get_conda_list_package_versions().get("ambertools", None)
