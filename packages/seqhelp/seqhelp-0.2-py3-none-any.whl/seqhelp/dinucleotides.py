"""Calculation of dinucleotide content and the cosine distances thereof between two sequences.

 Sped up with Numba to enable the calculations in seconds/minutes instead of hours.

Examples
--------
>>> left = seqhelp.dinucleotides.cache_dinucleotides("NC_004162", Path("path/to/NC_004162.fa.gz"))
>>> left
{'AT': 652, 'GT': 645, 'AA': 1033, 'GA': 880, 'TC': 535, 'CA': 973, 'CG': 603, 'TT': 466, 'AG': 911, 'GG': 697, 'TA': 630, 'TG': 760, 'GC': 749, 'CC': 742, 'AC': 921, 'CT': 628}
>>> right = seqhelp.dinucleotides.cache_dinucleotides("NC_012561", Path("path/to/NC_012561.fa.gz"))
>>> right
{'AT': 725, 'GT': 641, 'AA': 882, 'GA': 791, 'TC': 585, 'CA': 941, 'CG': 607, 'TT': 595, 'AG': 810, 'GG': 614, 'TA': 663, 'TG': 750, 'GC': 735, 'CC': 693, 'AC': 861, 'CT': 632}
>>> left_gc = seqhelp.gc_content.cache_gc_content("NC_004162", Path("path/to/NC_004162.fa.gz"))
>>> right_gc = seqhelp.gc_content.cache_gc_content("NC_012561", Path("path/to/NC_012561.fa.gz"))
>>> seqhelp.dinucleotides.dinucleotide_odds_ratio_cosine_distance(left, left_gc, right, right_gc)
0.02840407145550572

Or, with the class:
>>> import seqhelp
>>> paths = {"NC_004162": Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", "NC_012561": Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz"}
>>> dinucleotides = seqhelp.dinucleotides.Dinucleotides(paths)
>>> dinucleotides.distance("NC_004162", "NC_012561")
0.03534222425802276

Or, with parallelisation over the cosine distance of many entries:
>>> import seqhelp
>>> paths = {"NC_004162": Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", "NC_012561": Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz"}
>>> dinucleotides = seqhelp.dinucleotides.Dinucleotides(paths)
>>> dins = np.array([dinucleotides.transform(aid) for aid in ["NC_004162", "NC_012561"]])
>>> seqhelp.common.cosine_distances(dins)
array([[0.00000000e+00, 2.84040715e-02],
       [2.84040715e-02, 0.00000000e+00]])

"""

import functools
import gzip
import itertools
import json
from collections import defaultdict
from pathlib import Path
from typing import Final, Iterable

import numpy as np
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm

from . import gc_content
from .common import cosine_distance

DINUCLEOTIDE_TUPLES: Final = set((n1, n2) for n1 in "ACGT" for n2 in "ACGT")
DINUCLEOTIDES: Final = [f"{n1}{n2}" for (n1, n2) in DINUCLEOTIDE_TUPLES]


def _dinucleotide_generator(record: SeqRecord) -> Iterable[tuple[str, str]]:
    return itertools.pairwise(record.seq)


@functools.cache
def cache_dinucleotides(
    aid, path: Path, cache_dir: Path = Path("cache/dinucleotides")
):
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = (cache_dir / f"{aid}-dinucleotides").with_suffix(".json")

    if cache_path.is_file():
        with cache_path.open("r") as f:
            dinucleotides_ = json.load(f)
    else:
        if path.suffix == ".gz":
            with gzip.open(path, "rt") as f:
                records = SeqIO.parse(f, "fasta")
                dinucleotides_ = _count_dinucleotides(records)
        else:
            with path.open("r") as f:
                records = SeqIO.parse(f, "fasta")
                dinucleotides_ = _count_dinucleotides(records)

        with cache_path.open("w") as f:
            json.dump(dinucleotides_, f)

    return dinucleotides_


def _count_dinucleotides(records):
    dinucleotides__ = defaultdict(int)
    for rec in tqdm(
        records,
        desc="Iterating records to calculate dinucleotides",
        position=3,
        leave=False,
    ):
        for din in tqdm(
            _dinucleotide_generator(rec),
            desc=f"Iterating dinucleotides in record {rec.id}",
            position=4,
            leave=False,
            total=len(rec.seq) - 1,
        ):
            dinucleotides__[din] += 1
    dinucleotides_ = {
        f"{din[0]}{din[1]}": dinucleotides__[din] for din in DINUCLEOTIDE_TUPLES
    }
    return dinucleotides_


def dinucleotide_odds_ratio_cosine_distance(
    left_dinucleotides, left_gc, right_dinucleotides, right_gc
):
    left_odds_ratios = np.array(
        [
            left_dinucleotides[din]
            / (
                left_gc[_nucleotide_to_index(din[0])]
                * left_gc[_nucleotide_to_index(din[1])]
            )
            for din in DINUCLEOTIDES
        ]
    )
    left_odds_ratios = np.nan_to_num(left_odds_ratios, copy=False)
    right_odds_ratios = np.array(
        [
            right_dinucleotides[din]
            / (
                right_gc[_nucleotide_to_index(din[0])]
                * right_gc[_nucleotide_to_index(din[1])]
            )
            for din in DINUCLEOTIDES
        ]
    )
    right_odds_ratios = np.nan_to_num(right_odds_ratios, copy=False)

    return cosine_distance(left_odds_ratios, right_odds_ratios)


class Dinucleotides:
    """Calculate cosine similarity between dinucleotide odds ratios

    Dinucleotide odds ratio is as defined by Karlin and Burge in https://doi.org/10.1016/S0168-9525(00)89076-9
    """

    def __init__(self, path_dict, cache_dir: Path = Path("cache/dinucleotides")):
        """
        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        cache_dir : Path
            Location of cached dinucleotide content calculations on disk
        """
        self.path_dict = path_dict
        self.cache_dir = Path(cache_dir)

    def distance(self, left: str, right: str) -> float:
        left_gc = gc_content.cache_gc_content(left, self.path_dict[left], self.cache_dir / "gc")
        left_dinucleotides = cache_dinucleotides(left, self.path_dict[left], self.cache_dir)
        right_gc = gc_content.cache_gc_content(right, self.path_dict[right], self.cache_dir / "gc")
        right_dinucleotides = cache_dinucleotides(right, self.path_dict[right], self.cache_dir)

        return dinucleotide_odds_ratio_cosine_distance(
            left_dinucleotides, left_gc, right_dinucleotides, right_gc
        )

    def transform(self, aid: str) -> np.ndarray:
        """Transforms the aid into the corresponding array.

        Parameters
        ----------
        aid: str
            Aid to transform

        Returns
        -------
        np.ndarray
            Array of dinucleotide odds ratios, in a deterministic order
        """
        gc = gc_content.cache_gc_content(aid, self.path_dict[aid], self.cache_dir)
        dinucleotides_ = cache_dinucleotides(aid, self.path_dict[aid], self.cache_dir)
        transform_ = np.array(
            [
                dinucleotides_[din]
                / (gc[_nucleotide_to_index(din[0])] * gc[_nucleotide_to_index(din[1])])
                for din in DINUCLEOTIDES
            ]
        )
        transform_ = np.nan_to_num(transform_, copy=False)
        return transform_


def _nucleotide_to_index(nucleotide: str) -> int:
    if nucleotide == "A":
        return 0
    elif nucleotide == "C":
        return 1
    elif nucleotide == "G":
        return 2
    else:
        return 3
