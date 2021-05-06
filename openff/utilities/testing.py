from typing import Iterable, Optional, Union

import pytest

from openff.utilities.utils import has_executable, has_pkg


def skip_if_missing(pkg_name: str, reason: Optional[str] = None):
    """
    Helper function to generate a pytest.mark.skipif decorator
    for any package. This allows tests to be skipped if some
    optional dependency is not found.

    Parameters
    ----------
    pkg_name : str
        The name of the package that is required for a test(s)
    reason : str, optional
        Explanation of why the skipped it to be tested

    Returns
    -------
    requires_pkg : _pytest.mark.structures.MarkDecorator
        A pytest decorator that will skip tests if the package is not available
    """
    if not reason:
        reason = f"Package {pkg_name} is required, but was not found."
    requires_pkg = pytest.mark.skipif(not has_pkg(pkg_name), reason=reason)
    return requires_pkg


def skip_if_missing_exec(exec: Union[str, Iterable[str]]):
    """Helper function to generate a pytest.mark.skipif decorator
    if an executable(s) is not found."""
    if isinstance(exec, str):
        execs = [exec]
    else:
        execs = exec

    found_exec = False
    for exec in execs:
        found_exec = found_exec or has_executable(exec)

    reason = f"Package {str(exec)} is required, but was not found."
    mark = pytest.mark.skipif(not found_exec, reason=reason)
    return mark
