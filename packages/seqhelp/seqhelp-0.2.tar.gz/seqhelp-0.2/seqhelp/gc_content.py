"""Calculation of GC content and the cosine distances of GC content between two sequences.

 Sped up with Numba to enable the calculations in seconds/minutes instead of hours.

Examples
--------
>>> left = seqhelp.gc_content.cache_gc_content("NC_004162", Path("path/to/NC_004162.fa.gz"))
>>> left
array([3517, 2947, 2971, 2391])
>>> right = seqhelp.gc_content.cache_gc_content("NC_012561", Path("path/to/NC_012561.fa.gz"))
>>> right
array([3278, 2874, 2781, 2593])
>>> seqhelp.gc_content.get_gc_diff(left, right)
0.03534222425802276

Or, with the class:
>>> gc = seqhelp.gc_content.GC({"NC_004162": Path("path/to/NC_004162.fa.gz"), "NC_012561": Path("path/to/NC_012561.fa.gz")})
>>> gc.distance("NC_004162", "NC_012561")
0.03534222425802276

Or, with parallelisation over the cosine distance of many entries:
>>> gc = seqhelp.gc_content.GC({"NC_004162": Path("path/to/NC_004162.fa.gz"), "NC_012561": Path("path/to/NC_012561.fa.gz")})
>>> gcs = np.array([gc.transform(aid) for aid in ["NC_004162", "NC_012561"]])
>>> seqhelp.common.cosine_distances(gcs)
array([[0.00000000e+00, 3.53422243e-02],
       [3.53422243e-02, 0.00000000e+00]])

"""

import functools
import gzip
import json
from collections import Counter
from pathlib import Path

import numba
import numpy as np
from Bio import SeqIO

from .common import cosine_distance


@functools.cache
def cache_gc_content(
    aid, path: Path, cache_dir: Path = Path("cache/gc-content")
) -> np.ndarray:
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = (cache_dir / f"{aid}-gc").with_suffix(".json")

    if cache_path.is_file():
        with cache_path.open("r") as f:
            gc = json.load(f)
    else:
        if path.suffix == ".gz":
            with gzip.open(path, "rt") as f:
                records = SeqIO.parse(f, "fasta")
                seq = "".join([str(rec.seq) for rec in records])
        else:
            with path.open("r") as f:
                records = SeqIO.parse(f, "fasta")
                seq = "".join([str(rec.seq) for rec in records])

        gc = Counter(seq)
        with cache_path.open("w") as f:
            json.dump(gc, f)

    gc_ = np.array([gc.get(c, gc.get(c.lower(), 0)) for c in "ACGT"])
    return gc_


@numba.njit
def get_gc_diff(left_gc, right_gc):
    gc_i_a = left_gc / np.sum(left_gc)

    gc_j_a = right_gc / np.sum(right_gc)

    return cosine_distance(gc_i_a, gc_j_a)


class GC:
    """
    Calculate GC distance angular cosine distance
    """

    def __init__(self, path_dict, cache_dir: Path = Path("cache/gc-content")):
        """
        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        cache_dir : Path
            Location of cached GC content calculations on disk
        """
        self.path_dict = path_dict
        self.cache_dir = cache_dir

    def distance(self, left: str, right: str) -> float:
        left_gc = cache_gc_content(left, self.path_dict[left], self.cache_dir)
        right_gc = cache_gc_content(right, self.path_dict[right], self.cache_dir)

        return get_gc_diff(left_gc, right_gc)

    def transform(self, aid: str) -> np.ndarray:
        """Transforms the aid into the corresponding array.

        Parameters
        ----------
        aid: str
            Aid to transform

        Returns
        -------
        np.ndarray
            Array of gc content, in a deterministic order
        """
        gc_array = cache_gc_content(aid, self.path_dict[aid], self.cache_dir)
        gc_array = gc_array / np.sum(gc_array)
        return gc_array
