import errno
import importlib
import os
from contextlib import contextmanager
from functools import wraps
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Callable, Generator, Literal, Optional, TypeVar

from openff.utilities.exceptions import MissingOptionalDependencyError

if TYPE_CHECKING:
    from pathlib import Path

# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators

F = TypeVar("F", bound=Callable[..., Any])


def has_package(package_name: str) -> bool:
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


def requires_package(package_name: str) -> Callable[..., Any]:
    """
    Helper function to denote that a funciton requires some optional
    dependency. A function decorated with this decorator will raise
    `MissingOptionalDependencyError` if the package is not found by
    `importlib.import_module()`.

    Parameters
    ----------
    package_name : str
        The name of the module to be imported.

    Raises
    ------
    MissingOptionalDependencyError

    """

    def inner_decorator(function: F) -> F:
        @wraps(function)
        def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
            import importlib

            try:
                importlib.import_module(package_name)
            except ImportError:
                raise MissingOptionalDependencyError(library_name=package_name)
            except Exception as e:
                raise e

            return function(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return inner_decorator


def requires_oe_module(
    module_name: Literal["oechem", "oeomega", "oequacpac", "oeiupac", "oedepict"],
) -> Callable[..., Any]:
    """
    Helper function to denote that a funciton requires a particular OpenEye library.
    A function decorated with this decorator will raise `MissingOptionalDependencyError` if
    the module is not found by @requires_package or the module is not found to be
    licensed.

    Parameters
    ----------
    module_name : str
        The name of the OpenEye module to be imported.

    Raises
    ------
    MissingOptionalDependencyError
    """

    def inner_decorator(function: F) -> F:
        @requires_package(f"openeye.{module_name}")
        @wraps(function)
        def wrapper(*args, **kwargs):  # type: ignore
            oe_module = importlib.import_module(f"openeye.{module_name}")

            license_functions = {
                "oechem": "OEChemIsLicensed",
                "oequacpac": "OEQuacPacIsLicensed",
                "oeiupac": "OEIUPACIsLicensed",
                "oeomega": "OEOmegaIsLicensed",
                "oedepict": "OEDepictIsLicensed",
            }

            is_licensed = getattr(oe_module, license_functions[module_name])()

            if not is_licensed:
                raise MissingOptionalDependencyError(
                    library_name=f"openeye.{module_name}", license_issue=True
                )

            return function(*args, **kwargs)

        return wrapper  # type: ignore

    return inner_decorator


def has_executable(program_name: str) -> bool:
    import os

    def _is_executable(fpath: str) -> bool:
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
def temporary_cd(directory_path: Optional[str] = None) -> Generator[None, None, None]:
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


def get_data_dir_path(relative_path: str, package_name: str) -> str:
    """Get the full path to a directory within a module's tree.

    If no directory is found at `relative_path`, a second attempt will be made
    with `data/` preprended. If no directory is found at path, a NotADirectoryError
    is raised.

    Parameters
    ----------
    relative_path : str
        The relative path of the file to load.
    package_name : str
        The name of the package in which a file is to be loaded, i.e. "openff.toolkit" or "openff.evaluator".

    Returns
    -------
        The absolute path to the file.

    Raises
    ------
    NotADirectoryError

    See Also
    --------
    get_data_file_path, for getting the path to a particular file in a data directory.

    """
    from importlib_resources import files

    dir_path: "Path" = files(package_name) / relative_path

    if dir_path.is_dir():
        pass
    elif (files(package_name) / "data" / relative_path).is_dir():
        dir_path = files(package_name) / "data" / relative_path
    else:
        raise NotADirectoryError(
            f"Directory {relative_path} not found in {package_name}."
        )

    return dir_path.as_posix()


def get_data_file_path(relative_path: str, package_name: str) -> str:
    """Get the full path to one of the files in the data directory.

    If no file is found at `relative_path`, a second attempt will be made
    with `data/` preprended. If no files exist at either path, a FileNotFoundError
    is raised.

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

    See Also
    --------
    get_data_dir_path, for getting the path to a directory instead of an individual file.

    """
    from importlib_resources import files

    file_path: "Path" = files(package_name) / relative_path

    if not file_path.is_file():
        try_path = files(package_name) / f"data/{relative_path}"
        if try_path.is_file():
            file_path = try_path
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)

    return file_path.as_posix()
