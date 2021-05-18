from openff.utilities._version import get_versions  # type: ignore
from openff.utilities.utilities import (
    get_data_file_path,
    has_executable,
    has_package,
    requires_package,
    temporary_cd,
)

# Handle versioneer
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
