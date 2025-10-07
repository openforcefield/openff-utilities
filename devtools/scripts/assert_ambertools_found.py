import os
from shutil import which

try:
    assert which("sqm")
except AssertionError:
    os.system(f"ls {os.environ['CONDA_PREFIX']}/bin/")
