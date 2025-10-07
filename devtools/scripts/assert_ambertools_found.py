import os
from shutil import which

try:
    assert which('sqm')
except AssertionError as error:
    os.system(f"ls {os.environ['CONDA_PREFIX']}/bin/")
    raise error
