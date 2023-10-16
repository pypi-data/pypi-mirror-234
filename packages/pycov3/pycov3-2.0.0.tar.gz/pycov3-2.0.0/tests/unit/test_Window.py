import pytest
from src.pycov3.Sequence import Window


def test_valid_initialization():
    # Test valid initialization of Window
    window = Window(0, 10, "ATGCATCGTA")
    assert window.start == 0
    assert window.end == 10
    assert window.len == 10


def test_invalid_start():
    # Test initialization with an invalid start
    with pytest.raises(ValueError):
        Window(-1, 10, "ATGCATCGTA")


def test_invalid_end():
    # Test initialization with an invalid end
    with pytest.raises(ValueError):
        Window(0, 0, "ATGCATCGTA")


def test_invalid_sequence_length():
    # Test initialization with an invalid sequence length
    with pytest.raises(ValueError):
        Window(0, 10, "ATGC")


def test_get_window():
    # Test getting the subsequence represented by the window
    window = Window(2, 6, "ATGC")
    sub_seq = window.get_window("ATGCATCGTA")
    assert sub_seq == "GCAT"


def test_generate_windows():
    # Test generating windows
    windows = Window.generate_windows(30, 5, 10, 2)
    assert len(windows) == 6


def test_generate_windows_invalid():
    # Test generating windows with invalid parameters
    assert not Window.generate_windows(20, 5, 15, 2)


def test_calculate_GC_content():
    # Test calculating GC content
    gc_content = Window.calculate_GC_content("ATGCATCGTA")
    assert gc_content == 0.4


def test_calculate_GC_skew():
    # Test calculating GC skew
    gc_skew = Window.calculate_GC_skew("ATGCATCGTA")
    assert gc_skew == [0, 0, 1, 0, 0, 0, -1, 0, 0, 0]
