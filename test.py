import os
import pathlib
import shutil


print(os.environ["PATH"])

assert shutil.which("micromamba") is not None, "shutil could not fine executable"

assert pathlib.Path("/usr/local/bin/micromamba").is_file, "executable is not file-like"
assert os.access("/usr/local/bin/micromamba", os.X_OK), "os.access could not access executable"
