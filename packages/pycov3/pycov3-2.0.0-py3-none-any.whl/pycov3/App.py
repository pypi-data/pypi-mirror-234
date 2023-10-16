import logging
import math
from collections import OrderedDict
from typing import Dict, Iterator, List, Tuple, Union

from .Sequence import Contig


class Cov3Generator:
    def __init__(
        self,
        sam_generators: Dict[str, Iterator[Dict[str, Union[str, int]]]],
        fasta_generator: Iterator[Tuple[str, str]],
        sample: str,
        bin_name: str,
        window_params: Dict[str, int],
        mapq_cutoff: int,
        mapl_cutoff: int,
        max_mismatch_ratio: float,
    ) -> None:
        self.sam_generators = sam_generators
        self.fasta_generator = fasta_generator
        self.sample = sample
        self.bin_name = bin_name
        self.window_params = window_params
        self.mapq_cutoff = mapq_cutoff
        self.mapl_cutoff = mapl_cutoff
        self.max_mismatch_ratio = max_mismatch_ratio

        self.min_cov_window = 0.1
        self.min_window_count = 5

    def generate_cov3(self) -> Iterator[Dict[str, Union[str, int, float]]]:
        next_lines = OrderedDict(
            sorted(
                {name: next(sg, {}) for name, sg in self.sam_generators.items()}.items()
            )
        )

        for contig_name, seq in self.fasta_generator:
            contig = Contig(
                contig_name, seq, self.sample, self.bin_name, **self.window_params
            )
            logging.debug(f"Current contig: {contig_name}")

            for name, line in next_lines.items():
                mut_line = line
                coverages = {}
                while True:
                    if not mut_line:
                        break  # Generator is exhausted
                    if mut_line["reference_name"] == "*":
                        next_lines[name] = {}
                        break  # SAM file has no more mapped reads
                    if mut_line["reference_name"] != contig_name:
                        break  # This contig is unmapped by this SAM file
                    if contig.windows:
                        coverages = self.__update_coverages(
                            coverages,
                            mut_line,
                            contig.edge_length,
                            contig.window_step,
                        )
                    mut_line = next(self.sam_generators[name], {})

                next_lines[
                    name
                ] = mut_line  # Instead of updating with every iteration of the while loop
                if coverages:
                    for info in self.__log_cov_info(
                        contig,
                        coverages,
                        contig.edge_length,
                        contig.window_size,
                        contig.window_step,
                    ):
                        info["sample"] = name
                        info["contig"] = contig_name
                        info["length"] = contig.seq_len
                        yield info

    def __update_coverages(
        self,
        coverages: Dict[int, int],
        line: Dict[str, Union[str, int]],
        edge_length: int,
        window_step: int,
    ) -> Dict[int, int]:
        mapl = self.calculate_mapl(line["cigar"])
        if (
            line["mapping_quality"] >= self.mapq_cutoff
            and mapl >= self.mapl_cutoff
            and line["mismatch"] <= self.max_mismatch_ratio * mapl
        ):
            start_step = int((line["position"] - 1 - edge_length) / window_step)
            end_step = int((line["position"] - 1 + mapl - edge_length) / window_step)

            if start_step not in coverages:
                coverages[start_step] = 0
            coverages[start_step] += window_step - (
                (line["position"] - 1 - edge_length) % window_step
            )
            if end_step not in coverages:
                coverages[end_step] = 0
            coverages[end_step] += (
                line["position"] - 1 + mapl - edge_length
            ) % window_step

            for step in range(start_step + 1, end_step):
                if step not in coverages:
                    coverages[step] = 0
                coverages[step] += window_step

        return coverages

    def __log_cov_info(
        self,
        contig: Contig,
        coverages: Dict[int, int],
        edge_length: int,
        window_size: int,
        window_step: int,
    ) -> List[Dict[str, float]]:
        first_i = contig.windows[0].start
        last_i = contig.windows[-1].end
        first_step = int((first_i - 1 - edge_length) / window_step)
        last_step = int((last_i - 1 - edge_length) / window_step)

        cov_step = []
        cov_window_sum = 0
        qualified_info = []  # Information to output
        n = 0  # Window index

        for step in range(first_step, last_step):
            if step in coverages.keys():
                cov_step.append(coverages[step])
                cov_window_sum += coverages[step]
            else:
                cov_step.append(0)

            if len(cov_step) == window_size / window_step:
                avg_cov_window = cov_window_sum / window_size
                window = contig.windows[n]
                gc_content = window.gc_content
                n += 1
                cov_window_sum -= cov_step.pop(0)
                if avg_cov_window > self.min_cov_window:
                    log_cov = round(math.log(avg_cov_window) / math.log(2), 4)
                    qualified_info.append(
                        {"log_cov": log_cov, "GC_content": gc_content}
                    )

        if n >= self.min_window_count and len(qualified_info) == n:
            return qualified_info
        return []

    @staticmethod
    def calculate_mapl(cigar: str) -> int:
        operations = []
        current_length = ""

        if cigar == "*":
            return -1

        for char in cigar:
            if char.isdigit():
                current_length += char
            else:
                operations.append((int(current_length), char))
                current_length = ""

        return sum([n for n, c in operations if c == "M" or c == "D"]) - sum(
            [n for n, c in operations if c == "I"]
        )
