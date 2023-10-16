from pathlib import Path
from src.pycov3.File import SamFile
from tests.unit.utils import create_sample_sam_file


def test_sam_file_init():
    # Test SamFile initialization
    sam_file_path = Path("Akk_001.sam")
    create_sample_sam_file(sam_file_path)

    sam_file = SamFile(sam_file_path)
    assert sam_file.sample == "Akk"
    assert sam_file.bin_name == "001"


def test_sam_file_parse():
    # Test SamFile parse method
    sam_file_path = Path("Akk_001.sam")
    create_sample_sam_file(sam_file_path)

    sam_file = SamFile(sam_file_path)
    parsed_reads = list(sam_file.parse())

    assert len(parsed_reads) == 2
    assert parsed_reads[0]["read_name"] == "read1"
    assert parsed_reads[0]["flag"] == 0
    assert parsed_reads[0]["reference_name"] == "Contig1"
    assert parsed_reads[0]["position"] == 1
    assert parsed_reads[0]["mapping_quality"] == 30
    assert parsed_reads[0]["cigar"] == "30M"
    assert parsed_reads[0]["mismatch"] == 0


def test_sam_file_parse_contig_lengths():
    # Test SamFile parse_contig_lengths method
    sam_file_path = Path("Akk_001.sam")
    create_sample_sam_file(sam_file_path)

    sam_file = SamFile(sam_file_path)
    contig_lengths = sam_file.parse_contig_lengths()

    assert len(contig_lengths) == 1
    assert contig_lengths["Contig1"] == 100


def test_sam_file_write():
    # Test SamFile write method (not implemented)
    pass
