import logging
from pathlib import Path
from src.pycov3.Directory import SamDir, FastaDir, Cov3Dir


def test_sim_data():
    logging.basicConfig()
    logging.getLogger().setLevel(10)

    sim_fp = Path("sim")
    sams_fp = sim_fp / "sams"
    fastas_fp = sim_fp / "fastas"
    output_fp = sim_fp / "output"

    overwrite = True

    sam_d = SamDir(sams_fp, overwrite)

    window_params = {
        "window_size": 500,
        "window_step": 10,
        "edge_length": sam_d.calculate_edge_length(),
    }
    coverage_params = {
        "mapq_cutoff": None,
        "mapl_cutoff": None,
        "max_mismatch_ratio": None,
    }
    window_params = {k: v for k, v in window_params.items() if v is not None}
    coverage_params = {k: v for k, v in coverage_params.items() if v is not None}

    fasta_d = FastaDir(fastas_fp, overwrite)

    cov3_d = Cov3Dir(
        output_fp, overwrite, fasta_d.get_filenames(), window_params, coverage_params
    )

    cov3_d.generate(sam_d, fasta_d)

    # import shutil
    # shutil.copyfile(output_fp / "max_bin.002.cov3", "/mnt/d/Penn/pycov3/tests/data/sim/expected_output/max_bin.002.cov3")

    cov3_1 = cov3_d.get_bin("001")
    # cov3_2 = cov3_d.get_bin("002")

    sample_contigs_1 = list(cov3_1.parse_sample_contig())
    print(sample_contigs_1[0]["sample"])
    print(sample_contigs_1[0]["contig"])
    akk_001_k141_0_test(sample_contigs_1[0]["log_covs"])
    bfrag_001_k141_0_test(sample_contigs_1[1]["log_covs"])
    akk_001_k141_2_test(sample_contigs_1[2]["log_covs"])
    bfrag_001_k141_2_test(sample_contigs_1[3]["log_covs"])


def akk_001_k141_0_test(lc):
    assert sum(lc[: int(len(lc) / 2)]) < sum(lc[int(len(lc) / 2) :])


def bfrag_001_k141_0_test(lc):
    assert sum(lc[: int(len(lc) / 2)]) > sum(lc[int(len(lc) / 2) :])


def akk_001_k141_2_test(lc):
    assert (
        round(lc[0], 1) == round(lc[int(len(lc) / 2)], 1) == round(lc[len(lc) - 1], 1)
    )


def bfrag_001_k141_2_test(lc):
    assert sum(lc[: int(len(lc) / 2)]) < sum(lc[int(len(lc) / 2) :])
