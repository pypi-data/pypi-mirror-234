import shutil
import sys
import pytest
from pathlib import Path


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    base_fp = Path([fp for fp in sys.path if fp.endswith("pycov3")][0])

    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        shutil.copytree(base_fp / "tests" / "data" / "sim", Path(tmpdir) / "sim")
        yield
