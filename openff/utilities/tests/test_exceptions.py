import pytest

from openff.utilities.exceptions import MissingOptionalDependency, OpenFFException


def test_exceptions():
    with pytest.raises(
        MissingOptionalDependency,
        match="The required foobar module could not be imported.*"
        "Try installing.*conda-forge.*",
    ):
        raise MissingOptionalDependency(library_name="foobar")

    with pytest.raises(MissingOptionalDependency, match=".*barbaz.*missing license."):
        raise MissingOptionalDependency(library_name="barbaz", license_issue=True)

    with pytest.raises(OpenFFException):
        raise MissingOptionalDependency("numpy")
