import importlib
from typing import Optional

import pytest


def has_pkg(pkg_name: str):
    """
    Helper function to generically check if a package is installed. Intended
    to be used to check for optional dependencies.

    Parameters
    ----------
    pkg_name : str
        The name of the package to check the availability of

    Returns
    -------
    pkg_available : bool
        Boolean indicator if the package is available or not

    Examples
    --------
    >>> has_numpy = has_pkg('numpy')
    >>> has_numpy
    True
    >>> has_foo = has_pkg('other_non_installed_pkg')
    >>> has_foo
    False
    """
    try:
        importlib.import_module(pkg_name)
    except ModuleNotFoundError:
        return False
    return True


def requires_pkg(pkg_name: str, reason: Optional[str] = None):
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
