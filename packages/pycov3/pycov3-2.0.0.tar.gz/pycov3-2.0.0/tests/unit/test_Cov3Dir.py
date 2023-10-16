import os
from pathlib import Path
from src.pycov3.Directory import Cov3Dir

window_params = {
    "window_size": 500,
    "window_step": 10,
    "edge_length": 10,
}
coverage_params = {
    "mapq_cutoff": None,
    "mapl_cutoff": None,
    "max_mismatch_ratio": None,
}
window_params = {k: v for k, v in window_params.items() if v is not None}
coverage_params = {k: v for k, v in coverage_params.items() if v is not None}

fns = ["max_bin.001", "max_bin.002"]


def test_cov3_dir_init():
    # Define a temporary directory path for testing
    temp_dir = Path("cov3_dir")
    os.makedirs(temp_dir)

    cov3_dir = Cov3Dir(temp_dir, False, fns, window_params, coverage_params)

    assert len(cov3_dir.files) == 2


def test_cov3_dir_get_bin():
    # Define a temporary directory path for testing
    temp_dir = Path("cov3_dir")
    os.makedirs(temp_dir)

    cov3_dir = Cov3Dir(temp_dir, False, fns, window_params, coverage_params)

    assert cov3_dir.get_bin("001").bin_name == "001"
