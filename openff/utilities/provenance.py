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

    if has_executable("pixi"):
        conda_command = "pixi list --color never"
    elif has_executable("micromamba"):
        conda_command = "micromamba list"
    elif has_executable("mamba"):
        conda_command = "mamba list"
    elif has_executable("conda"):
        conda_command = "conda list"
    else:
        warnings.warn(
            "No conda/mamba/micromamba executable found. Unable to determine package versions.",
            CondaExecutableNotFoundWarning,
        )
        return dict()

    output = list(
        filter(
            lambda x: len(x) > 0,
            subprocess.check_output(conda_command.split()).decode().split("\n"),
        )
    )

    package_versions = {}

    # pixi has a brief header, others list "here's the path", etc
    for output_line in output[3 - has_executable("pixi") * 2 : -1]:
        # The output format of `conda`/`mamba list` and `micromamba list` are different.
        # See https://github.com/openforcefield/openff-utilities/issues/65
        # Some setups may also have even more custom headers, which could cause this to bubble up a ValueError.
        # See https://github.com/openforcefield/openff-utilities/issues/41
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

    try:
        return _get_conda_list_package_versions().get("ambertools", None)
    except (
        ValueError,  # Issue 98
        subprocess.CalledProcessError,  # Issue 101
    ):
        from openff.utilities.warnings import CondaExecutableNotFoundWarning

        warnings.warn(
            "Something went wrong parsing the output of `conda list` or similar. Unable to "
            "determine AmberTools version, returning None.",
            CondaExecutableNotFoundWarning,
        )

        return None
