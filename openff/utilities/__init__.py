from importlib.metadata import version

from openff.utilities.exceptions import MissingOptionalDependencyError
from openff.utilities.provenance import get_ambertools_version
from openff.utilities.testing import skip_if_missing, skip_if_missing_exec
from openff.utilities.utilities import (
    get_data_dir_path,
    get_data_file_path,
    has_executable,
    has_package,
    requires_oe_module,
    requires_package,
    temporary_cd,
)

__all__ = (
    "MissingOptionalDependencyError",
    "get_ambertools_version",
    "get_data_dir_path",
    "get_data_file_path",
    "has_executable",
    "has_package",
    "requires_oe_module",
    "requires_package",
    "skip_if_missing",
    "skip_if_missing_exec",
    "temporary_cd",
)

__version__ = version("openff.utilities")
