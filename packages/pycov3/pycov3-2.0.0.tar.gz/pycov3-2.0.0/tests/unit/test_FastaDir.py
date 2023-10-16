import os
from pathlib import Path
from src.pycov3.Directory import FastaDir
from tests.unit.utils import create_sample_fasta_file

dummy_fasta_files = [
    "max_bin.001.fasta",
    "max_bin.002.fa",
    "max_bin.003.fna",
    "max_bin.004.fasta",
]


def test_fasta_dir_init():
    # Define a temporary directory path for testing
    temp_dir = Path("fasta_dir")
    os.makedirs(temp_dir)

    for dummy_file in dummy_fasta_files:
        create_sample_fasta_file(temp_dir / dummy_file)

    # Initialize a FastaDir instance
    fasta_dir = FastaDir(temp_dir, False)

    # Test if the FastaDir object is created correctly
    assert len(fasta_dir.files) == 4  # Assuming 4 dummy files were created


def test_fasta_dir_get_bin():
    # Define a temporary directory path for testing
    temp_dir = Path("fasta_dir")
    os.makedirs(temp_dir)

    for dummy_file in dummy_fasta_files:
        create_sample_fasta_file(temp_dir / dummy_file)

    # Initialize a FastaDir instance
    fasta_dir = FastaDir(temp_dir, False)

    # Test the get_bin method
    fasta_file = fasta_dir.get_bin("004")

    assert fasta_file.sample == "max_bin"
    assert fasta_file.bin_name == "004"
