import pytest

from openff.utilities.exceptions import (
    MissingOptionalDependency,
    MissingOptionalDependencyError,
    OpenFFException,
)


def test_exceptions():
    with pytest.raises(
        MissingOptionalDependencyError,
        match="The required foobar module could not be imported.*"
        "Try installing.*conda-forge.*",
    ):
        raise MissingOptionalDependencyError(library_name="foobar")

    with pytest.raises(
        MissingOptionalDependencyError, match=".*barbaz.*missing license."
    ):
        raise MissingOptionalDependencyError(library_name="barbaz", license_issue=True)

    with pytest.raises(OpenFFException):
        raise MissingOptionalDependencyError("numpy")


def test_missing_optional_dependency_deprecation():
    with pytest.raises(MissingOptionalDependency):
        with pytest.warns(UserWarning, match="DEP"):
            raise MissingOptionalDependency("foobar")
