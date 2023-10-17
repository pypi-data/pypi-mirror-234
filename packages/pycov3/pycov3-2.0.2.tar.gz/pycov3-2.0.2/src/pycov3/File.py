import logging
from abc import ABC, abstractmethod
from itertools import groupby
from pathlib import Path
from typing import Dict, Iterator, List, Tuple, Union

from .App import Cov3Generator


class File(ABC):
    def __init__(self, fp: Path) -> None:
        super().__init__()
        self.fp = fp

    def exists(self) -> bool:
        if not self.fp.exists():
            logging.error(f"{self.fp} does not exist")
            return False
        if self.fp.stat().st_size == 0:
            logging.error(f"{self.fp} is empty")
            return False
        return True

    @abstractmethod
    def parse(self) -> None:
        pass

    @abstractmethod
    def write(self) -> None:
        pass


class FastaFile(File):
    def __init__(self, fp: Path) -> None:
        super().__init__(fp)

        try:
            stem = self.fp.stem.split(".")
            self.sample = stem[0]
            self.bin_name = stem[1]
        except IndexError:
            raise ValueError(
                f"FASTA filename {self.fp} not of format {{sample}}.{{bin_name}}.fasta/.fa/.fna"
            )

    def parse(self) -> Iterator[Tuple[str, str]]:
        with open(self.fp) as f:
            faiter = (x[1] for x in groupby(f, lambda line: line[0] == ">"))

            for header in faiter:
                # drop the ">"
                header_str = header.__next__()[1:].strip().split(" ")[0]

                # join all sequence lines to one.
                seq_str = "".join(s.strip() for s in faiter.__next__())

                yield (header_str, seq_str)

    def write(self):
        pass


class SamFile(File):
    def __init__(self, fp: Path) -> None:
        super().__init__(fp)
        stem = self.fp.stem.split("_")
        self.sample = stem[0]
        self.bin_name = stem[1].split(".")[0]

    def parse(self) -> Iterator[Dict[str, Union[str, int]]]:
        with open(self.fp, "r") as f:
            for line in f:
                if line.startswith("@"):
                    continue  # Skip header lines
                fields = line.split("\t")
                read_name = fields[0]
                flag = int(fields[1])
                reference_name = fields[2]
                position = int(fields[3])
                mapping_quality = int(fields[4])
                cigar = fields[5]
                mismatch = 0
                try:
                    if reference_name != "*":
                        # Find XM field for mismatches
                        for i in [13, 14, 15, 12, 11]:
                            if fields[i].split(":") == "XM":
                                mismatch = int(fields[i].split(":")[2])
                                break
                except IndexError:
                    pass

                parsed_read = {
                    "read_name": read_name,
                    "flag": flag,
                    "reference_name": reference_name,
                    "position": position,
                    "mapping_quality": mapping_quality,
                    "cigar": cigar,
                    "mismatch": mismatch,
                }
                yield parsed_read

    def parse_contig_lengths(self) -> Dict[str, int]:
        lengths = {}
        with open(self.fp, "r") as sam_file:
            for line in sam_file:
                if line.startswith("@"):
                    if line.startswith("@SQ"):
                        contig_name = line.split("\t")[1][3:]
                        contig_length = int(line.split("\t")[2][3:])
                        lengths[contig_name] = contig_length
                else:
                    break

        return lengths

    def write(self):
        pass


class Cov3File(File):
    def __init__(
        self,
        fp: Path,
        bin_name: str,
        mapq_cutoff: int = 5,
        mapl_cutoff: int = 50,
        max_mismatch_ratio: float = 0.03,
    ) -> None:
        super().__init__(fp)
        self.bin_name = bin_name

        self.mapq_cutoff = mapq_cutoff
        self.mapl_cutoff = mapl_cutoff
        self.max_mismatch_ratio = max_mismatch_ratio

        if not (0 <= self.mapq_cutoff <= 30):
            raise ValueError(
                f"MapQ cutoff of {self.mapq_cutoff} is not between 0 and 30"
            )
        if not (30 <= self.mapl_cutoff <= 80):
            raise ValueError(
                f"MapL cutoff of {self.mapl_cutoff} is not between 30 and 80"
            )
        if not (0.01 <= self.max_mismatch_ratio <= 0.3):
            raise ValueError(
                f"Max mismatch ratio of {self.max_mismatch_ratio} is not between 0.01 and 0.30"
            )

    def parse(self) -> Iterator[Dict[str, Union[str, int, float]]]:
        with open(self.fp) as f:
            f.readline()  # Skip header
            for line in f.readlines():
                fields = line.split(",")
                yield {
                    "log_cov": float(fields[0]),
                    "GC_content": float(fields[1]),
                    "sample": fields[2],
                    "contig": fields[3],
                    "length": int(fields[4]),
                }

    def parse_sample_contig(self) -> Iterator[Dict[str, Union[str, int, List[float]]]]:
        with open(self.fp) as f:
            data_dict = {}
            f.readline()  # Skip header
            for line in f.readlines():
                fields = line.split(",")
                parsed_line = {
                    "log_cov": float(fields[0]),
                    "GC_content": float(fields[1]),
                    "sample": fields[2],
                    "contig": fields[3],
                    "length": int(fields[4]),
                }

                sample = parsed_line["sample"]
                contig = parsed_line["contig"]

                if (sample, contig) not in data_dict:
                    data_dict[(sample, contig)] = {
                        "sample": sample,
                        "contig": contig,
                        "contig_length": parsed_line["length"],
                        "log_covs": [],
                        "GC_contents": [],
                    }

                data_dict[(sample, contig)]["log_covs"].append(parsed_line["log_cov"])
                data_dict[(sample, contig)]["GC_contents"].append(
                    parsed_line["GC_content"]
                )

            for values in data_dict.values():
                yield values

    def write(
        self,
        sams: List[SamFile],
        fasta: FastaFile,
        window_params: Dict[str, int],
    ) -> None:
        sam_generators = {sam.fp.stem: sam.parse() for sam in sams}
        cov3_generator = Cov3Generator(
            sam_generators,
            fasta.parse(),
            fasta.sample,
            fasta.bin_name,
            window_params,
            self.mapq_cutoff,
            self.mapl_cutoff,
            self.max_mismatch_ratio,
        )

        self.write_generator(cov3_generator)

    def write_generator(self, cov3_generator: Cov3Generator) -> None:
        with open(self.fp, "w") as f_out:
            f_out.write(
                ",".join(["log_cov", "GC_content", "sample", "contig", "length"])
            )  # Write header
            f_out.write("\n")
            for line in cov3_generator.generate_cov3():
                f_out.write(",".join([str(v) for v in line.values()]))
                f_out.write("\n")
