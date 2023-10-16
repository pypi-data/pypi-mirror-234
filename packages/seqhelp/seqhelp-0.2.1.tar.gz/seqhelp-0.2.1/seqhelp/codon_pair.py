"""Calculation of codon pairs and the cosine distances thereof between two sequences.

 Sped up with Numba to enable the calculations in seconds/minutes instead of hours.

Examples
--------
>>> left = seqhelp.codon_pair.get_codon_pair_score_array("NC_004162", Path("path/to/NC_004162.fa.gz"))
>>> left
{'AT': 652, 'GT': 645, 'AA': 1033, 'GA': 880, 'TC': 535, 'CA': 973, 'CG': 603, 'TT': 466, 'AG': 911, 'GG': 697, 'TA': 630, 'TG': 760, 'GC': 749, 'CC': 742, 'AC': 921, 'CT': 628}
>>> right = seqhelp.codon_pair.get_codon_pair_score_array("NC_012561", Path("path/to/NC_012561.fa.gz"))
>>> right
{'AT': 725, 'GT': 641, 'AA': 882, 'GA': 791, 'TC': 585, 'CA': 941, 'CG': 607, 'TT': 595, 'AG': 810, 'GG': 614, 'TA': 663, 'TG': 750, 'GC': 735, 'CC': 693, 'AC': 861, 'CT': 632}
>>> seqhelp.common.cosine_distance(left, right)
0.855109251212154

Or, with the class:
>>> import seqhelp
>>> paths = {"NC_004162": Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", "NC_012561": Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz"}
>>> codon_pair = seqhelp.codon_pair.CPSCorrelation(paths)
>>> codon_pair.distance("NC_004162", "NC_012561")
0.855109251212154

Or,
>>> codon_pair = seqhelp.codon_pair.CPSCorrelation()
>>> codon_pair.distance(Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz")

Or, with parallelisation over the cosine distance of many entries:
>>> import seqhelp
>>> paths = {"NC_004162": Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", "NC_012561": Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz"}
>>> codon_pair = seqhelp.codon_pair.CPSCorrelation(paths)
>>> codon_pairs = np.array([codon_pair.transform(aid) for aid in ["NC_004162", "NC_012561"]])
>>> seqhelp.common.cosine_distances(codon_pairs)
array([[0.00000000e+00, 8.55109251e-01],
       [8.55109251e-01, 0.00000000e+00]])

"""

import functools
import gzip
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, Final, Iterable, NewType, Tuple

import numba
import numpy as np

# noinspection PyPackageRequirements
from Bio import SeqIO

# noinspection PyPackageRequirements
from Bio.SeqRecord import SeqRecord

from . import codon
from .codon import CodonTable, VALID_CODONS, _SYNONYMOUS_CODONS
from .common import cosine_distance

CodonPairTable = NewType("CodonPairTable", dict)
CodonPairScoreTable = NewType("CodonPairScoreTable", dict)
AminoAcidTable = NewType("AminoAcidTable", dict)
AminoAcidPairTable = NewType("AminoAcidPairTable", dict)


def generate_codon_pair_score_table(
    codon_counts: CodonTable,
    codon_pair_counts: CodonPairTable,
) -> CodonPairScoreTable:
    """Generate codon pair score table from the codon and codon pair counts.

    Defined for each codon pair as the frequency of the codon pair normalised by
    the frequency of each individual codon and the frequencies of the amino acid pair.

    Parameters
    ----------
    codon_counts: CodonTable
        Codon counts.
    codon_pair_counts: CodonPairTable
        Codon pair counts.

    Returns
    -------
    CodonPairScoreTable
        Codon pair score table.

    References
    ----------
    [1] https://doi.org/10.1126/science.1155761
    """
    aa_counts = _count_amino_acids(codon_counts)

    aa_pair_counts = _count_amino_acid_pairs(codon_pair_counts)

    cpst = defaultdict(float)

    for codon_pair, counts in codon_pair_counts.items():
        first_codon, second_codon = _split_codon_pair(codon_pair)
        if len(first_codon) == 0 or len(second_codon) == 0:
            continue

        first_aa, second_aa = (
            _CODON_AA_TABLE[first_codon],
            _CODON_AA_TABLE[second_codon],
        )
        aa_pair = first_aa + second_aa

        codon_frequency_normalisation = (
            codon_counts[first_codon]
            * codon_counts[second_codon]
            / (aa_counts[first_aa] * aa_counts[second_aa])
        ) * aa_pair_counts[aa_pair]

        cpst[codon_pair] = np.log(counts / codon_frequency_normalisation)

    return cpst


def _count_amino_acid_pairs(codon_pair_counts: CodonPairTable) -> AminoAcidPairTable:
    aa_pair_counts = defaultdict(float)
    for codon_pair, counts in codon_pair_counts.items():
        first_codon, second_codon = _split_codon_pair(codon_pair)

        if len(first_codon) == 0 or len(second_codon) == 0:
            continue

        first_aa, second_aa = (
            _CODON_AA_TABLE[first_codon],
            _CODON_AA_TABLE[second_codon],
        )

        aa_pair = first_aa + second_aa
        aa_pair_counts[aa_pair] += counts

    return aa_pair_counts


def _count_amino_acids(codon_counts: CodonTable) -> AminoAcidTable:
    aa_counts = defaultdict(float)
    for aa, synonymous_codons in _SYNONYMOUS_CODONS.items():
        aa_counts[aa] = sum(codon_counts[codon] for codon in synonymous_codons)
    return aa_counts


def count_codon_pairs(records: Iterable[SeqRecord]) -> CodonPairTable:
    """Counts the codon pairs in records.  Assumed to be in-frame.

    Parameters
    ----------
    records: Iterable[SeqRecord]
        Record to count codon pairs in.

    Returns
    -------
    CodonPairTable
        Counts of the codon pairs

    References
    ----------
    [1] https://doi.org/10.1126/science.1155761
    """
    codon_pairs = defaultdict(float)

    for record in records:
        for codon_pair in _codon_pair_generator(record):
            codon_pairs[codon_pair] += 1

    return codon_pairs


_illegal_codon_pairs_discovered = defaultdict(set)


def _codon_pair_generator(record: SeqRecord) -> Iterable[str]:
    sequence = str(record.seq)
    for codon_pair_start in range(0, len(sequence) - 3, 3):
        codon_pair_end = codon_pair_start + 6
        codon_pair = sequence[codon_pair_start:codon_pair_end]

        first_codon, second_codon = _split_codon_pair(codon_pair)
        if first_codon not in VALID_CODONS or second_codon not in VALID_CODONS:
            if codon_pair not in _illegal_codon_pairs_discovered[record.id]:
                logging.warning(f"Illegal codon pair {codon_pair} in gene: {record.id}")
                _illegal_codon_pairs_discovered[record.id].add(codon_pair)
            continue

        yield codon_pair


def _split_codon_pair(codon_pair: str) -> Tuple[str, str]:
    return codon_pair[:3], codon_pair[3:]


def codon_pair_bias_from_counts(
    cpst: CodonPairScoreTable, codon_pair_count: CodonPairTable
) -> float:
    """Calculates the codon pair bias for a given codon pair count.

    Defined as the arithmetic mean of the codon pair scores of the codon pairs.

    Parameters
    ----------
    cpst: CodonPairScoreTable
        The codon pair score table for each codon pair.
    codon_pair_count: CodonPairTable
        Codon pairs to score.

    Returns
    -------
    float
        Codon pair bias.

    References
    ----------
    [1] https://doi.org/10.1126/science.1155761
    """
    n_codon_pairs = 0
    codon_pair_sum = 0
    for codon_pair, count in codon_pair_count.items():
        codon_pair_sum += cpst[codon_pair] * count
        n_codon_pairs += count

    return codon_pair_sum / (n_codon_pairs - 1)


@numba.njit
def codon_pair_bias_from_counts_(
    cpst: np.ndarray, codon_pair_count: np.ndarray
) -> float:
    """Calculates the codon pair bias for a given codon pair count.

    Defined as the arithmetic mean of the codon pair scores of the codon pairs.

    Parameters
    ----------
    cpst: np.ndarray
        The codon pair score table for each codon pair.
    codon_pair_count: np.ndarray
        Codon pairs to score.

    Returns
    -------
    float
        Codon pair bias.

    References
    ----------
    [1] https://doi.org/10.1126/science.1155761
    """
    n_codon_pairs = 0
    codon_pair_sum = 0
    for codon_pair_i, count in enumerate(codon_pair_count):
        codon_pair_sum += cpst[codon_pair_i] * count
        n_codon_pairs += count

    return codon_pair_sum / (n_codon_pairs - 1)


def codon_pair_bias(cpst: CodonPairScoreTable, records: Iterable[SeqRecord]) -> float:
    """Calculates the codon pair bias for a gene.

    Defined as the arithmetic mean of the codon pair scores of the codon pairs in records.

    Parameters
    ----------
    cpst: CodonPairScoreTable
        The codon pair score table for each codon pair.
    records: Iterable[SeqRecord]
        Records to score.

    Returns
    -------
    float
        Codon pair bias for the records.

    References
    ----------
    [1] https://doi.org/10.1126/science.1155761
    """
    n_codon_pairs = 0
    codon_pair_sum = 0
    for record in records:
        for codon_pair in _codon_pair_generator(record):
            codon_pair_sum += cpst[codon_pair]
            n_codon_pairs += 1

    return codon_pair_sum / (n_codon_pairs - 1)


def cache_codon_pair_count(
    aid: str, record_path: Path, cache_dir: Path = Path("cache/codon-pairs")
) -> CodonPairTable:
    """Caches the codon pair counts, or fetches them from disk if previously calculated.

    Parameters
    ----------
    aid: str
        Unique identifier for the records.
    record_path: Path
        Path to record.
    cache_dir: Path
        Path to where codon counts are cached.

    Returns
    -------
    CodonPairTable
        Count of codon pairs in record_path.

    References
    ----------
    [1] https://doi.org/10.1126/science.1155761
    """
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = (cache_dir / f"{aid}-codon-pairs").with_suffix(".json")

    if cache_path.is_file():
        with cache_path.open("r") as f:
            codon_pair_count = json.load(f)
    else:
        logging.info(f"Counting codon pairs for {aid}")
        if record_path.suffix == ".gz":
            with gzip.open(record_path, "rt") as f:
                records = SeqIO.parse(f, "fasta")
                codon_pair_count = count_codon_pairs(records)
        else:
            with record_path.open("r") as f:
                records = SeqIO.parse(f, "fasta")
                codon_pair_count = count_codon_pairs(records)

        with cache_path.open("w") as f:
            json.dump(codon_pair_count, f)

    return codon_pair_count


@functools.cache
def cache_codon_pair_count_array(aid: str, record_path: Path, cache_dir: Path = Path("cache/codon-pairs")) -> np.ndarray:
    codon_pair_count = cache_codon_pair_count(aid, record_path, cache_dir)

    return np.array(
        [
            codon_pair_count.get(first_codon + second_codon, 0.0)
            for first_codon in codon.VALID_CODONS
            for second_codon in codon.VALID_CODONS
        ]
    )


@functools.cache
def get_codon_pair_score_table(aid: str, path: Path, cache_path: Path = Path("cache/codon-pairs")) -> CodonPairScoreTable:
    codon_counts = codon.cache_codon_count(aid, path, cache_path / "codons")
    codon_pair_counts = cache_codon_pair_count(aid, path, cache_path)
    cpst = generate_codon_pair_score_table(codon_counts, codon_pair_counts)
    return cpst


@functools.cache
def get_codon_pair_score_array(aid: str, path: Path, cache_path: Path = Path("cache/codon-pairs")) -> np.ndarray:
    codon_counts = codon.cache_codon_count(aid, path, cache_path / "codons")
    codon_pair_counts = cache_codon_pair_count(aid, path, cache_path)
    cpst = generate_codon_pair_score_table(codon_counts, codon_pair_counts)

    return np.array(
        [
            cpst.get(first_codon + second_codon, 0.0)
            for first_codon in codon.VALID_CODONS
            for second_codon in codon.VALID_CODONS
        ]
    )


class CPB:
    """Calculate distance as the codon pair bias.

    As defined by Coleman et al. in https://doi.org/10.1126/science.1155761

    Assume sequences gives are in frame.
    """

    def __init__(self, path_dict, cache_dir: Path = Path("cache/codon-pairs")):
        """
        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        """
        self.path_dict = path_dict
        self.cache_dir = Path(cache_dir)

    def distance(self, left: str, right: str) -> float:
        cpst = get_codon_pair_score_array(right, self.path_dict[right], self.cache_dir)

        left_codon_pair_counts = cache_codon_pair_count_array(
            left, self.path_dict[left], self.cache_dir
        )

        return codon_pair_bias_from_counts_(cpst, left_codon_pair_counts)

    def transform(self, aid):
        return aid


class CPSCorrelation:
    """Calculate distance as the cosine distance of codon pair scores.

    Codon pair scores are as defined by Coleman et al. in https://doi.org/10.1126/science.1155761

    This assumes sequences gives are in frame.
    """

    def __init__(self, path_dict: Dict[str, Path] = None, cache_dir: Path = Path("cache/codon-pairs")):
        """

        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        """
        self.path_dict = path_dict
        self.cache_dir = Path(cache_dir)

    @functools.singledispatchmethod
    def distance(self, left, right):
        return 0.0

    @distance.register
    def _(self, left: str, right: str):
        if right not in self.path_dict or self.path_dict[right] is None:
            logging.info(f"{right} not in path_dict, or is None")
            return np.inf
        elif left not in self.path_dict or self.path_dict[left] is None:
            logging.info(f"{left} not in path_dict, or is None")
            return np.inf

        left_cpst = get_codon_pair_score_array(left, self.path_dict[left], self.cache_dir)
        right_cpst = get_codon_pair_score_array(right, self.path_dict[right], self.cache_dir)

        return self.distance(left_cpst, right_cpst)

    @distance.register
    def _(self, left_p: Path, right_p: Path):
        left_cpst = get_codon_pair_score_array(left_p.stem, left_p, self.cache_dir)
        right_cpst = get_codon_pair_score_array(right_p.stem, right_p, self.cache_dir)
        return self.distance(left_cpst, right_cpst)

    @distance.register(dict)
    def _(
        self,
        left_cpst: CodonPairScoreTable,
        right_cpst: CodonPairScoreTable,
    ):

        right_cps_array = np.array(
            [
                right_cpst[first_codon + second_codon]
                for first_codon in codon.VALID_CODONS
                for second_codon in codon.VALID_CODONS
            ]
        )
        left_cps_array = np.array(
            [
                left_cpst[first_codon + second_codon]
                for first_codon in codon.VALID_CODONS
                for second_codon in codon.VALID_CODONS
            ]
        )

        return cosine_distance(left_cps_array, right_cps_array)

    @distance.register
    def _(
        self,
        left_cpst: np.ndarray,
        right_cpst: np.ndarray,
    ):

        return cosine_distance(left_cpst, right_cpst)

    def transform(self, aid) -> np.ndarray:
        """Transforms the aid into the corresponding array.

        Parameters
        ----------
        aid: str
            Aid to transform

        Returns
        -------
        np.ndarray
            Array of codon pair scores, in a deterministic order
        """

        return get_codon_pair_score_array(aid, self.path_dict[aid])


_CODON_AA_TABLE: Final = {
    codon: aa
    for aa, synonymous_codons in _SYNONYMOUS_CODONS.items()
    for codon in synonymous_codons
}
