from openff.utilities.testing import skip_if_missing, skip_if_missing_exec


def test_skips():
    assert not skip_if_missing("numpy").args[0]
    assert skip_if_missing("numpynumpy").args[0]

    assert not skip_if_missing_exec("python").args[0]
    assert skip_if_missing_exec("python4").args[0]
    assert not skip_if_missing_exec(["python", "python4"]).args[0]
    assert skip_if_missing_exec(["python4", "python5"]).args[0]
