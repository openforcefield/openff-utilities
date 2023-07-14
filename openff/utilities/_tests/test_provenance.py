import importlib

import pytest

from openff.utilities.provenance import get_ambertools_version


def test_get_ambertools_version_found():
    # Skip if ambertools is not installed.
    pytest.importorskip("parmed")

    assert get_ambertools_version() is not None


def test_get_ambertools_version_not_found():
    try:
        importlib.import_module("parmed")
    except ImportError:
        assert get_ambertools_version() is None
        return

    pytest.skip("only run when ambertools is not installed.")
