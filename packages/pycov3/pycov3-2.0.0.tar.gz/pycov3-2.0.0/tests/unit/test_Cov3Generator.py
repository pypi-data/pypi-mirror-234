import os
from pathlib import Path
from src.pycov3.Directory import SamDir
from src.pycov3.File import SamFile, FastaFile
from src.pycov3.App import Cov3Generator
from src.pycov3.Sequence import Contig
from tests.unit.utils import (
    create_sample_fasta_file,
    create_sample_sam_file,
)


def test_cov3_generator_generate_cov3():
    # Test generate_cov3() method of Cov3Generator
    sam_file_path = Path("sams/Akk_001.sam")
    os.makedirs("sams", exist_ok=True)
    create_sample_sam_file(sam_file_path)
    sam_dir = SamDir(Path("sams"), True)

    fasta_file_path = Path("max_bin.001.fa")
    create_sample_fasta_file(fasta_file_path)
    fasta_file = FastaFile(fasta_file_path)

    cov3_generator = Cov3Generator(
        {s.fp.stem: s.parse() for s in sam_dir.files},
        fasta_file.parse(),
        "Akk",
        "001",
        {
            "window_size": 500,
            "window_step": 10,
            "edge_length": sam_dir.calculate_edge_length(),
        },
        1,
        30,
        0.03,
    )

    assert (
        list(cov3_generator.generate_cov3()) == []
    )  # Test data is too small for window_size min


def test_cov3_file_update_coverages():
    # Test cov3 file update_coverages utility
    sam_file_path = Path("Akk_001.sam")
    create_sample_sam_file(sam_file_path)
    sam_file = SamFile(sam_file_path)
    sam_lines = list(sam_file.parse())

    cov3_generator = Cov3Generator(
        [sam_file.parse()],
        None,
        "Akk",
        "001",
        {"window_size": 500, "window_step": 10, "edge_length": 5},
        1,
        30,
        0.03,
    )

    coverages = {}

    for line in sam_lines:
        coverages = cov3_generator._Cov3Generator__update_coverages(
            coverages, line, 2, 2
        )

    assert coverages == {
        -1: 2,
        14: 2,
        0: 2,
        1: 2,
        2: 2,
        3: 2,
        4: 4,
        5: 4,
        6: 4,
        7: 4,
        8: 4,
        9: 4,
        10: 4,
        11: 4,
        12: 4,
        13: 4,
        19: 0,
        15: 2,
        16: 2,
        17: 2,
        18: 2,
    }


def test_cov3_file_log_cov_info():
    # Test cov3 file update_coverages utility
    fasta_file_path = Path("max_bin.001.fa")
    create_sample_fasta_file(fasta_file_path)
    fasta_file = FastaFile(fasta_file_path)
    fasta_records = list(fasta_file.parse())

    cov3_generator = Cov3Generator(
        [],
        fasta_file.parse(),
        "Akk",
        "001",
        {"window_size": 500, "window_step": 10, "edge_length": 5},
        1,
        30,
        0.03,
    )

    contig = Contig(
        fasta_records[0][0], fasta_records[0][1] * 10, "Akk0", "001", 5, 500, 10
    )
    coverages = {}
    for i in range(-1, 599):
        coverages[i] = 2
    coverages[599] = 0

    info = cov3_generator._Cov3Generator__log_cov_info(contig, coverages, 5, 500, 10)
    assert info == [
        {"log_cov": -2.3219, "GC_content": 0.496},
        {"log_cov": -2.3219, "GC_content": 0.496},
        {"log_cov": -2.3219, "GC_content": 0.5},
        {"log_cov": -2.3219, "GC_content": 0.504},
        {"log_cov": -2.3219, "GC_content": 0.504},
        {"log_cov": -2.3219, "GC_content": 0.502},
        {"log_cov": -2.3219, "GC_content": 0.498},
        {"log_cov": -2.3219, "GC_content": 0.496},
        {"log_cov": -2.3219, "GC_content": 0.496},
        {"log_cov": -2.3219, "GC_content": 0.5},
        {"log_cov": -2.3219, "GC_content": 0.504},
        {"log_cov": -2.3219, "GC_content": 0.504},
        {"log_cov": -2.3219, "GC_content": 0.502},
        {"log_cov": -2.3219, "GC_content": 0.498},
        {"log_cov": -2.3219, "GC_content": 0.496},
        {"log_cov": -2.3219, "GC_content": 0.498},
        {"log_cov": -2.3219, "GC_content": 0.502},
    ]


def test_cov3_file_calculate_mapl():
    # Test cov3 file mapping length calculation
    assert Cov3Generator.calculate_mapl("250M") == 250
    assert Cov3Generator.calculate_mapl("100M50I100M") == 150
    assert Cov3Generator.calculate_mapl("200D50I") == 150
    assert Cov3Generator.calculate_mapl("250H") == 0
    assert Cov3Generator.calculate_mapl("*") == -1
