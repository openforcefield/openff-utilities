"""
openff-utilities
A collection of miscellaneous utility functions used throughout the OpenFF stack
"""

# Add imports here
from .utilities import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
