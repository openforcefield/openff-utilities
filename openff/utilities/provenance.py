import functools
import subprocess
from typing import Dict, Optional


@functools.lru_cache()
def _get_conda_list_package_versions() -> Dict[str, str]:
    """Returns the versions of any packages found while executing `conda list`."""
    from openff.utilities.exceptions import CondaExecutableNotFoundError
    from openff.utilities.utilities import has_executable

    if has_executable("micromamba"):
        conda_executable = "micromamba"
    elif has_executable("mamba"):
        conda_executable = "mamba"
    elif has_executable("conda"):
        conda_executable = "conda"
    else:
        raise CondaExecutableNotFoundError()

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
    """Attempts to retrieve the version of the currently installed AmberTools."""

    return _get_conda_list_package_versions().get("ambertools", None)
