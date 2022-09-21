import pytest

from openff.utilities.exceptions import MissingOptionalDependencyError, OpenFFError


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

    with pytest.raises(OpenFFError):
        raise MissingOptionalDependencyError("numpy")
