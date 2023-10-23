from openff.utilities._version import get_versions
from openff.utilities.exceptions import MissingOptionalDependencyError
from openff.utilities.provenance import get_ambertools_version
from openff.utilities.testing import skip_if_missing, skip_if_missing_exec
from openff.utilities.utilities import (
    get_data_file_path,
    has_executable,
    has_package,
    requires_oe_module,
    requires_package,
    temporary_cd,
)

__all__ = (
    "get_versions",
    "get_ambertools_version",
    "has_executable",
    "has_package",
    "requires_oe_module",
    "requires_package",
    "skip_if_missing",
    "skip_if_missing_exec",
    "temporary_cd",
    "MissingOptionalDependencyError",
    "get_data_file_path",
)

versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
