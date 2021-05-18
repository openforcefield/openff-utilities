import errno
import importlib
import os
from contextlib import contextmanager
from functools import wraps
from tempfile import TemporaryDirectory
from typing import Optional

from openff.utilities.exceptions import MissingOptionalDependency


def has_package(package_name: str):
    """
    Helper function to generically check if a Python package is installed.
    Intended to be used to check for optional dependencies.

    Parameters
    ----------
    package_name : str
        The name of the Python package to check the availability of

    Returns
    -------
    package_available : bool
        Boolean indicator if the package is available or not

    Examples
    --------
    >>> has_numpy = has_package('numpy')
    >>> has_numpy
    True
    >>> has_foo = has_package('other_non_installed_package')
    >>> has_foo
    False
    """
    try:
        importlib.import_module(package_name)
    except ModuleNotFoundError:
        return False
    return True


def requires_package(package_name: str):
    """
    Helper function to denote that a funciton requires some optional
    dependency. A function decorated with this decorator will raise
    `MissingDependencyError` if the package is not found by
    `importlib.import_module()`.

    Parameters
    ----------
    package_name : str
        The directory path to enter within the context

    Raises
    ------
    MissingDependencyError

    """

    def inner_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            import importlib

            try:
                importlib.import_module(package_name)
            except (ImportError, ModuleNotFoundError):
                raise MissingOptionalDependency(library_name=package_name)
            except Exception as e:
                raise e

            return function(*args, **kwargs)

        return wrapper

    return inner_decorator


def has_executable(program_name: str) -> bool:
    import os

    def _is_executable(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program_name)
    if fpath:
        if _is_executable(program_name):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program_name)
            if _is_executable(exe_file):
                return True

    return False


@contextmanager
def temporary_cd(directory_path: Optional[str] = None):
    """Temporarily move the current working directory to the path
    specified. If no path is given, a temporary directory will be
    created, moved into, and then destroyed when the context manager
    is closed.

    Parameters
    ----------
    directory_path: str, optional

    Returns
    -------

    """

    if directory_path is not None and len(directory_path) == 0:
        yield
        return

    old_directory = os.getcwd()

    try:

        if directory_path is None:

            with TemporaryDirectory() as new_directory:
                os.chdir(new_directory)
                yield

        else:

            os.chdir(directory_path)
            yield

    finally:
        os.chdir(old_directory)


def get_data_file_path(relative_path: str, package_name: str) -> str:
    """Get the full path to one of the files in the data directory.

    Parameters
    ----------
    relative_path : str
        The relative path of the file to load.
    package_name : str
        The name of the package in which a file is to be loaded, i.e.
        "openff.toolkit" or "openff.evaluator"

    Returns
    -------
        The absolute path to the file.

    Raises
    ------
    FileNotFoundError
    """

    from pkg_resources import resource_filename

    file_path = resource_filename(package_name, os.path.join("data", relative_path))

    if not os.path.exists(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)

    return file_path