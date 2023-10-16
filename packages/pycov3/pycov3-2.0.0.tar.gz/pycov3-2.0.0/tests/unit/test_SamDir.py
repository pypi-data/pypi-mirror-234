import os
from pathlib import Path
from src.pycov3.Directory import SamDir
from tests.unit.utils import create_sample_sam_file

dummy_sam_files = [
    "sample1_001.sam",
    "sample2_002.sam",
    "sample2_001.sam",
    "sample1_002.sam",
]


def test_sam_dir_init():
    # Define a temporary directory path for testing
    temp_dir = Path("sam_dir")
    os.makedirs(temp_dir)

    for dummy_file in dummy_sam_files:
        create_sample_sam_file(temp_dir / dummy_file)

    sam_dir = SamDir(temp_dir, False)

    assert len(sam_dir.files) == 4  # Assuming 4 dummy files were created


def test_sam_dir_get_bin():
    # Define a temporary directory path for testing
    temp_dir = Path("sam_dir")
    os.makedirs(temp_dir)

    for dummy_file in dummy_sam_files:
        create_sample_sam_file(temp_dir / dummy_file)

    sam_dir = SamDir(temp_dir, False)

    # Test the get_bin method
    sam_files = sam_dir.get_bin("001")

    assert len(sam_files) == 2
    assert sam_files[0].bin_name == "001"


def test_sam_dir_calculate_edge_length():
    # Define a temporary directory path for testing
    temp_dir = Path("sam_dir")
    os.makedirs(temp_dir)

    for dummy_file in dummy_sam_files:
        create_sample_sam_file(temp_dir / dummy_file)

    sam_dir = SamDir(temp_dir, False)

    window_edge_length = sam_dir.calculate_edge_length()

    assert window_edge_length == 30
