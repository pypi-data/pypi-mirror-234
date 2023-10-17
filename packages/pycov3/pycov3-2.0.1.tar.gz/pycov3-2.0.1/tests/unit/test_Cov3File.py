from pathlib import Path
from src.pycov3.File import Cov3File
from tests.unit.utils import create_sample_cov3_file


def test_cov3_file_init():
    # Test cov3 file initialization
    cov3_file = Cov3File(Path("max_bin.001.cov3"), "001")
    assert cov3_file.bin_name == "001"


def test_cov3_file_parse():
    # Test cov3 file parse
    cov3_fp = Path("max_bin.001.cov3")
    create_sample_cov3_file(cov3_fp)
    cov3_file = Cov3File(cov3_fp, "001")

    cov3_vals = list(cov3_file.parse())

    assert len(cov3_vals) == 4
    assert cov3_vals[0]["log_cov"] == 1.234
    assert cov3_vals[0]["GC_content"] == 0.567
    assert cov3_vals[0]["sample"] == "sample1"
    assert cov3_vals[0]["contig"] == "contig1"
    assert cov3_vals[0]["length"] == 100


def test_cov3_file_parse_sample_contig():
    # Test cov3 file parse by sample and contig
    cov3_fp = Path("max_bin.001.cov3")
    create_sample_cov3_file(cov3_fp)
    cov3_file = Cov3File(cov3_fp, "001")

    cov3_vals = list(cov3_file.parse_sample_contig())

    assert len(cov3_vals) == 3
    assert cov3_vals[0]["sample"] == "sample1"
    assert cov3_vals[0]["contig"] == "contig1"
    assert len(cov3_vals[0]["log_covs"]) == 2
