import pytest
from src.pycov3.Sequence import Contig


def test_valid_initialization():
    # Test valid initialization of Contig
    contig = Contig("Name", "ATGC", "Sample", "001", 10)
    assert contig.name == "Name"
    assert contig.seq_len == 4
    assert contig.sample == "Sample"
    assert contig.bin_name == "001"
    assert contig.edge_length == 10
    assert contig.window_size == 5000
    assert contig.window_step == 100


def test_invalid_window_step():
    # Test initialization with an invalid window step
    with pytest.raises(ValueError):
        Contig("Name", "ATGC", "Sample", "Bin", 10, window_step=5)


def test_invalid_window_size():
    # Test initialization with an invalid window size
    with pytest.raises(ValueError):
        Contig("Name", "ATGC", "Sample", "Bin", 10, window_size=100)


def test_invalid_window_size_step_relationship():
    # Test initialization with invalid window size and step relationship
    with pytest.raises(ValueError):
        Contig("Name", "ATGC", "Sample", "Bin", 10, window_size=200, window_step=150)


def test_invalid_window_size_divisibility():
    # Test initialization with window size not divisible by window step
    with pytest.raises(ValueError):
        Contig("Name", "ATGC", "Sample", "Bin", 10, window_size=1000, window_step=150)


def test_generate_windows():
    # Test generating windows
    contig = Contig(
        "Name", "ATGCGATCG" * 100, "Sample", "Bin", 5, window_size=500, window_step=100
    )
    assert len(contig.windows) == 4


def test_no_windows():
    # Test no windows when sequence length is insufficient
    contig = Contig("Name", "ATG", "Sample", "Bin", 5)
    assert len(contig.windows) == 0
