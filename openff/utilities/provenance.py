import functools
import re
import subprocess
from typing import Dict, Optional


@functools.lru_cache()
def _get_conda_list_package_versions() -> Dict[str, str]:
    """Returns the versions of any packages found while executing `conda list`."""
    import os

    from openff.utilities.exceptions import CondaExecutableNotFoundError
    from openff.utilities.utilities import has_executable

    print([*os.environ["PATH"].split(os.pathsep)])

    raise Exception("Trigger")

    if has_executable("mamba"):
        conda_executable = "mamba"
    elif has_executable("conda"):
        conda_executable = "conda"
    elif has_executable("micromamba"):
        conda_executable = "micromamba"
    else:
        raise CondaExecutableNotFoundError()

    output = subprocess.check_output([conda_executable, "list"]).decode().split("\n")

    package_versions = {}

    for output_line in output[3:-1]:
        package_name, package_version, *_ = re.split(" +", output_line)
        package_versions[package_name] = package_version

    return package_versions


def get_ambertools_version() -> Optional[str]:
    """Attempts to retrieve the version of the currently installed AmberTools."""

    return _get_conda_list_package_versions().get("ambertools", None)
