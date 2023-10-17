import logging
from abc import ABC
from pathlib import Path
from typing import Dict, List, Union

from .File import FastaFile, SamFile, Cov3File


class Directory(ABC):
    def __init__(self, fp: Path, overwrite: bool) -> None:
        super().__init__()
        self.fp = fp.resolve()
        self.overwrite = overwrite
        self.files = []

        if not fp.is_dir() and fp.exists():
            raise ValueError(f"{self.fp} is not a directory")

    def get_filenames(self) -> List[str]:
        return [".".join(f.fp.name.split(".")[:-1]) for f in self.files]


class FastaDir(Directory):
    def __init__(self, fp: Path, overwrite: bool) -> None:
        super().__init__(fp, overwrite)

        self.files = [
            FastaFile(x)
            for x in self.fp.iterdir()
            if str(x).endswith((".fasta", ".fa", ".fna"))
        ]
        if not self.files:
            raise ValueError(
                f"No files found ending in .fasta, .fa, or .fna in {self.fp}"
            )

    def get_bin(self, bin_name: str) -> FastaFile:
        fasta_l = [f for f in self.files if f.bin_name == bin_name]
        if len(fasta_l) != 1:
            raise ValueError(
                f"Found 0 or more than 1 matches for bin {bin_name} in FASTAs"
            )
        return fasta_l[0]


class SamDir(Directory):
    def __init__(self, fp: Path, overwrite: bool) -> None:
        super().__init__(fp, overwrite)

        self.files = [SamFile(x) for x in self.fp.iterdir() if str(x).endswith(".sam")]
        if not self.files:
            raise ValueError(f"No files found ending in .sam in {self.fp}")

    def calculate_edge_length(self) -> int:
        edge_length = 0
        for sam in self.files:
            checks = 0
            for line in sam.parse():
                cutoff = 0
                for index, char in enumerate(line["cigar"]):
                    if not char.isdigit():
                        cutoff = index
                        break

                try:
                    cigar_val = int(line["cigar"][:cutoff])
                    if cigar_val > edge_length:
                        edge_length = cigar_val
                except ValueError:
                    logging.debug(f"Couldn't parse CIGAR value of {line['cigar']}")
                    break

                checks += 1
                if checks > 100:
                    break

        return edge_length

    def get_bin(self, bin_name: str) -> List[SamFile]:
        return [s for s in self.files if s.bin_name == bin_name]


class Cov3Dir(Directory):
    def __init__(
        self,
        fp: Path,
        overwrite: bool,
        fns: List[str],
        window_params: Dict[str, int],
        coverage_params: Dict[str, Union[int, float]],
    ) -> None:
        super().__init__(fp, overwrite)
        self.window_params = window_params

        if not fp.exists():
            logging.info(f"{self.fp} does not exist, creating it now")
            self.fp.mkdir(parents=True, exist_ok=True)
        if any(self.fp.iterdir()) and not self.overwrite:
            raise ValueError(
                f"{self.fp} is a non-empty directory, please either point output to an empty or non-existent directory or run with the overwrite flag"
            )

        self.files = [
            Cov3File(fp / f"{fn}.cov3", fn.split(".")[-1], **coverage_params)
            for fn in fns
        ]

    def generate(self, sam_d: SamDir, fasta_d: FastaDir) -> None:
        for cov3 in self.files:
            cov3.write(
                sam_d.get_bin(cov3.bin_name),
                fasta_d.get_bin(cov3.bin_name),
                self.window_params,
            )

    def get_bin(self, bin_name: str) -> Cov3File:
        result = [c for c in self.files if c.bin_name == bin_name]
        assert len(result) == 1, "There should be exactly one cov3 file for each bin"
        return result[0]
