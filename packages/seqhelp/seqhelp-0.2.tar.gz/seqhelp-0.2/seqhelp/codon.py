"""Calculation of relative synonymous codon usage and the cosine distances thereof between two sequences.

Sped up with Numba to enable the calculations in seconds/minutes instead of hours.

Examples
--------
>>> left = seqhelp.codon.generate_rscu_array("NC_004162", Path("path/to/NC_004162.fa.gz"))
>>> left
array([0.74452555, 1.19075145, 1.46715328, 0.78461538, 0.97260274,
       1.00411523, 0.89230769, 0.62992126, 1.17647059, 0.51666667,
       1.0617284 , 1.28395062, 0.95172414, 1.27692308, 1.15      ,
       0.8516129 , 0.87603306, 1.40740741, 1.1       , 0.35036496,
       0.68275862, 1.05555556, 1.02057613, 0.78014184, 0.60891089,
       1.13207547, 1.2       , 1.21985816, 1.36551724, 0.91970803,
       0.80924855, 0.64197531, 1.1023622 , 1.13385827, 1.49315068,
       1.20812183, 1.66336634, 1.13580247, 1.1483871 , 0.74452555,
       0.9       , 1.04615385, 1.13385827, 1.05445545, 1.77372263,
       0.82352941, 0.94444444, 1.0617284 , 0.9245283 , 1.11538462,
       0.79187817, 0.83950617, 1.12396694, 0.95890411, 0.78712871,
       0.57534247, 1.        , 1.02475248, 0.54320988, 0.94339623,
       0.88461538, 0.86138614, 1.13333333, 1.        ])
>>> right = seqhelp.codon.generate_rscu_array("NC_012561", Path("path/to/NC_012561.fa.gz"))
>>> right
array([0.79704797, 1.03448276, 0.86346863, 1.19111111, 0.81818182,
       0.9516129 , 0.67555556, 0.97222222, 1.10429448, 0.79207921,
       0.82634731, 0.79041916, 0.75949367, 1.28      , 0.95049505,
       0.95364238, 0.97435897, 1.2754491 , 0.77124183, 1.10701107,
       0.83544304, 1.03636364, 1.32258065, 0.99082569, 0.78358209,
       0.93925234, 1.33333333, 1.00917431, 1.40506329, 1.2398524 ,
       0.96551724, 1.0239521 , 0.94444444, 1.19444444, 1.13636364,
       0.92753623, 1.41044776, 1.        , 1.04635762, 1.01845018,
       1.22875817, 0.85333333, 0.88888889, 1.00746269, 0.97416974,
       0.89570552, 0.96363636, 1.13173653, 1.14953271, 1.22302158,
       1.07246377, 0.72580645, 1.02564103, 1.20454545, 1.00746269,
       0.84090909, 1.        , 0.60447761, 0.95209581, 0.91121495,
       0.77697842, 1.18656716, 0.92409241, 1.        ])
>>> seqhelp.common.cosine_distance(left, right)
0.16652628662258662

Or, with the class:
>>> import seqhelp
>>> paths = {"NC_004162": Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", "NC_012561": Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz"}
>>> codon = seqhelp.codon.RSCUCorrelation(paths)
>>> codon.distance("NC_004162", "NC_012561")
0.16652628662258662

Or, with parallelisation over the cosine distance of many entries:
>>> import seqhelp
>>> paths = {"NC_004162": Path.home() / "data" / "togaviridae" / "NC_004162.fa.gz", "NC_012561": Path.home() / "data" / "togaviridae" / "NC_012561.fa.gz"}
>>> codon = seqhelp.codon.RSCUCorrelation(paths)
>>> codons = np.array([codon.transform(aid) for aid in ["NC_004162", "NC_012561"]])
>>> seqhelp.common.cosine_distances(codons)
array([[0.00000000e+00, 1.66526287e-01],
       [1.66526287e-01, 0.00000000e+00]])

"""

import functools
import gzip
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, Final, Iterable, NewType

import numba
import numpy as np

# noinspection PyPackageRequirements
from Bio import SeqIO

# noinspection PyPackageRequirements
from Bio.SeqRecord import SeqRecord

from .common import cosine_distance

CodonTable = NewType("CodonTable", dict[str, float])
RSCUTable = NewType("RSCUTable", dict[str, float])
RelativeAdaptivenessTable = NewType("RelativeAdaptivenessTale", dict)


def generate_relative_adaptiveness_table(
    rscu_table: RSCUTable,
) -> RelativeAdaptivenessTable:
    """Generates the relative adaptiveness table as specified by Sharp and Li, termed $w$ by them.

    For each codon this is defined as the codon's relative synonymous codon usage divided by the maximum
    relative synonymous codon usage of the synonymous codons.  $w_{ij} = RSCU_{ij} / max_l RSCU{il}$

    Parameters
    ----------
    rscu_table: RSCUTable
        The relative synonymous codon usage table.

    Returns
    -------
    RelativeAdaptivenessTable
        The relative adaptiveness table.

    References
    ----------
    [1] https://doi.org/10.1093/nar/15.3.1281
    """
    rat = defaultdict(float)

    for synonymous_codons in _SYNONYMOUS_CODONS.values():
        rcsu_max = max(rscu_table[codon] for codon in synonymous_codons)
        for codon in synonymous_codons:
            rat[codon] = rscu_table[codon] / rcsu_max

    return rat


def generate_rscu_table(codon_count: CodonTable) -> RSCUTable:
    """Generates the Relative synonymous codon usage from the codon counts.

    Defined for each codon as the codon count over the average codon count.

    Parameters
    ----------
    codon_count: CodonTable
        The counts of each codon.

    Returns
    -------
    RSCUTable
        The relative synonymous codon usage of each codon.

    References
    ----------
    [1] https://doi.org/10.1093/nar/15.3.1281
    """
    rcsu = defaultdict(float)

    for synonymous_codons in _SYNONYMOUS_CODONS.values():
        expected_frequency = sum(
            codon_count[codon] for codon in synonymous_codons
        ) / len(synonymous_codons)

        for codon in synonymous_codons:
            rcsu[codon] = codon_count[codon] / expected_frequency

    return rcsu


@functools.cache
def generate_rscu_array(aid: str, path: Path, cache_dir: Path = Path("cache/codon")) -> np.ndarray:
    codon_count = cache_codon_count(aid, path, cache_dir)
    rscu = generate_rscu_table(codon_count)

    return np.array([rscu[codon] for codon in VALID_CODONS])


def count_codons(records: Iterable[SeqRecord]) -> CodonTable:
    """Counts the codon in the records.  Each sequence is assumed to be in-frame.

    Parameters
    ----------
    records: Iterable[SeqRecord]
        All records that the codon usage is calculated for.

    Returns
    -------
    CodonTable
        Count of each codon.

    References
    ----------
    [1] https://doi.org/10.1093/nar/15.3.1281
    """
    codon_count = defaultdict(float)
    for record in records:
        for codon in _codon_generator(record):
            codon_count[codon] += 1

    # From Sharp and Li:
    # "Note that if a certain codon is never used in the reference set
    # then the CAI for any other gene in which that codon appears becomes zero.
    # To overcome this problem we assign a value of 0.5 to any X
    # that would otherwise be zero."
    for codon in VALID_CODONS:
        if codon_count[codon] == 0:
            codon_count[codon] = 0.5

    return codon_count


_illegal_codons_discovered = defaultdict(set)


def _codon_generator(record: SeqRecord) -> Iterable[str]:
    sequence = str(record.seq)
    for codon_start in range(0, len(sequence), 3):
        codon_end = codon_start + 3
        codon = sequence[codon_start:codon_end]
        if codon not in VALID_CODONS:
            if codon not in _illegal_codons_discovered[record.id]:
                logging.warning(f"Illegal codon {codon} in gene: {record.id}")
                _illegal_codons_discovered[record.id].add(codon)

            continue

        yield codon


def codon_adaptation_index_from_counts(rat, codon_counts):
    """Calculates the codon adaptation index for a codon counts.

    Defined as the geometric mean of the relative adaptiveness of the codons.

    Parameters
    ----------
    rat: RelativeAdaptivenessTable
        The relative adaptiveness table to use as reference.
    codon_counts: Dict[str, int]
        The codons to calculate codon adaptation for.

    Returns
    -------
    float
        The codon adaptation index.

    References
    ----------
    [1] https://doi.org/10.1093/nar/15.3.1281
    """

    n_codons = 0
    cai_log_sum = 0.0

    for codon, count in codon_counts.items():
        # Exclude these codons, as stated by Sharp and Li:
        # "... the number of AUG and UGG codons are subtracted
        # from L, since the RSCU value, for AUG and UGG are both
        # fixed at 1.0, and so do not contribute to the CAI."
        if codon in {"ATG", "TGG"}:
            continue

        if rat[codon] != 0:
            cai_log_sum += np.log(rat[codon]) * count
            n_codons += count

    return np.exp(cai_log_sum / n_codons)


@numba.njit
def _codon_adaptation_index_from_counts(
    rat_array: np.ndarray, codon_counts_array: np.ndarray
):
    n_codons = 0
    cai_log_sum = 0.0
    for codon_i, count in enumerate(codon_counts_array):
        if rat_array[codon_i] != 0:
            cai_log_sum += np.log(rat_array[codon_i]) * count
            n_codons += count

    return np.exp(cai_log_sum / n_codons)


def codon_adaptation_index(
    rat: RelativeAdaptivenessTable, records: Iterable[SeqRecord]
) -> float:
    """Calculates the codon adaptation index for a given set of records, assumed to be in-frame.

    Defined as the geometric mean of the relative adaptiveness of the codons used in the records .

    Parameters
    ----------
    rat: RelativeAdaptivenessTable
        The relative adaptiveness table to use as reference.
    records: Iterable[SeqRecord]
        The records to calculate CAI for.

    Returns
    -------
    float
        The codon adaptation index for the records.

    References
    ----------
    [1] https://doi.org/10.1093/nar/15.3.1281
    """

    n_codons = 0
    cai_log_sum = 0.0

    for record in records:
        for codon in _codon_generator(record):
            # Exclude these codons, as stated by Sharp and Li:
            # "... the number of AUG and UGG codons are subtracted
            # from L, since the RSCU value, for AUG and UGG are both
            # fixed at 1.0, and so do not contribute to the CAI."
            if codon in {"ATG", "TGG"}:
                continue

            if rat[codon] != 0:
                cai_log_sum += np.log(rat[codon])
                n_codons += 1

    return np.exp(cai_log_sum / n_codons)


@functools.cache
def cache_codon_count(
    aid: str, record_path: Path, cache_dir: Path = Path("cache/codon")
) -> CodonTable:
    """Caches the codon counts, or fetches them from disk if previously calculated.

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
    CodonTable
        Count of codons in record_path.
    """
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = (cache_dir / f"{aid}-codons").with_suffix(".json")

    if cache_path.is_file():
        with cache_path.open("r") as f:
            codon_count = json.load(f)
    else:
        logging.info(f"Counting codons for {aid}")
        if record_path.suffix == ".gz":
            with gzip.open(record_path, "rt") as f:
                records = SeqIO.parse(f, "fasta")
                codon_count = count_codons(records)
        else:
            with record_path.open("r") as f:
                records = SeqIO.parse(f, "fasta")
                codon_count = count_codons(records)

        with cache_path.open("w") as f:
            json.dump(codon_count, f)

    return codon_count


@functools.cache
def cache_codon_count_array(aid: str, path: Path, cache_dir: Path = Path("cache/codon")) -> np.ndarray:
    codon_counts = cache_codon_count(aid, path, cache_dir)
    return np.array(
        [codon_counts[codon] for codon in VALID_CODONS if codon not in EXCLUDE_CODONS]
    )


@functools.cache
def cache_rat_array(aid: str, path: Path, cache_dir: Path = Path("cache/codon")) -> np.ndarray:
    codon_count = cache_codon_count(aid, path, cache_dir)
    rscu_table = generate_rscu_table(codon_count)
    rat = generate_relative_adaptiveness_table(rscu_table)

    return np.array(
        [rat[codon] for codon in VALID_CODONS if codon not in EXCLUDE_CODONS]
    )


class CAI:
    """
    Class for calculating the codon adaptation distance. Assumes all sequences given are in-frame.

    As defined by Sharp and Li in https://doi.org/10.1093/nar/15.3.1281.

    Most of this exists in the biopython package, but since it raises an error
    on incomplete codons, we can't use it.  This would be reasonable, but I'm putting
    that responsibility on the user instead.  Specifically, it's a problem since the CDS
    from genbank sometimes is incomplete and contains a lot of N characters.
    Rather than going through and checking every gene, we're assuming the general codon usage is the
    still preserved.

    Distance here is 1 - CAI.  So a distance of 0 means a perfect CAI and adaption to the host.

    """

    def __init__(self, path_dict):
        """
        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        """
        self.path_dict = path_dict

    def distance(self, left: str, right: str) -> float:
        rat_array = cache_rat_array(right, self.path_dict[right])

        codon_count = cache_codon_count_array(left, self.path_dict[left])

        return 1 - _codon_adaptation_index_from_counts(rat_array, codon_count)

    def transform(self, aid):
        return aid


class RSCUCorrelation:
    """
    Class for distances based on correlation of Relative Synonymous Codon Usage. Assumes all sequences given are in-frame.

    Relative synonymous codon usage is as defined by Sharp and Li in https://doi.org/10.1093/nar/15.3.1281.

    Distance is (1 - RSCU correlation) / 2

    """

    def __init__(self, path_dict: Dict[str, Path] = None, cache_dir: Path = "cache/codon"):
        """
        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        cache_dir : Path
            Location of cached codon usage on disk
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

        right_rscu_array = generate_rscu_array(right, self.path_dict[right], self.cache_dir)
        left_rscu_array = generate_rscu_array(left, self.path_dict[left], self.cache_dir)

        return self.distance(left_rscu_array, right_rscu_array)

    @distance.register
    def _(self, left: Path, right: Path):
        right_rscu_array = generate_rscu_array(right.stem, right)
        left_rscu_array = generate_rscu_array(left.stem, left)

        return self.distance(left_rscu_array, right_rscu_array)

    @distance.register(dict)
    def _(self, left_rscu_table: RSCUTable, right_rscu_table: RSCUTable):

        left_rscu_array = np.array([left_rscu_table[codon_] for codon_ in VALID_CODONS])
        right_rscu_array = np.array(
            [right_rscu_table[codon_] for codon_ in VALID_CODONS]
        )

        return cosine_distance(left_rscu_array, right_rscu_array)

    @distance.register
    def _(self, left_rscu_array: np.ndarray, right_rscu_array: np.ndarray):
        return cosine_distance(left_rscu_array, right_rscu_array)

    def transform(self, aid: str) -> np.ndarray:
        """Transforms the aid into the corresponding array.

        Parameters
        ----------
        aid: str
            Aid to transform

        Returns
        -------
        np.ndarray
            Array of relative synonymous codon usage, in a deterministic order
        """
        return generate_rscu_array(aid, self.path_dict[aid])


_SYNONYMOUS_CODONS: Final = {
    "CYS": ["TGT", "TGC"],
    "ASP": ["GAT", "GAC"],
    "SER": ["TCT", "TCG", "TCA", "TCC", "AGC", "AGT"],
    "GLN": ["CAA", "CAG"],
    "MET": ["ATG"],
    "ASN": ["AAC", "AAT"],
    "PRO": ["CCT", "CCG", "CCA", "CCC"],
    "LYS": ["AAG", "AAA"],
    "STOP": ["TAG", "TGA", "TAA"],
    "THR": ["ACC", "ACA", "ACG", "ACT"],
    "PHE": ["TTT", "TTC"],
    "ALA": ["GCA", "GCC", "GCG", "GCT"],
    "GLY": ["GGT", "GGG", "GGA", "GGC"],
    "ILE": ["ATC", "ATA", "ATT"],
    "LEU": ["TTA", "TTG", "CTC", "CTT", "CTG", "CTA"],
    "HIS": ["CAT", "CAC"],
    "ARG": ["CGA", "CGC", "CGG", "CGT", "AGG", "AGA"],
    "TRP": ["TGG"],
    "VAL": ["GTA", "GTC", "GTG", "GTT"],
    "GLU": ["GAG", "GAA"],
    "TYR": ["TAT", "TAC"],
}

VALID_CODONS: Final = {
    "TGT",
    "TGC",
    "GAT",
    "GAC",
    "TCT",
    "TCG",
    "TCA",
    "TCC",
    "AGC",
    "AGT",
    "CAA",
    "CAG",
    "ATG",
    "AAC",
    "AAT",
    "CCT",
    "CCG",
    "CCA",
    "CCC",
    "AAG",
    "AAA",
    "TAG",
    "TGA",
    "TAA",
    "ACC",
    "ACA",
    "ACG",
    "ACT",
    "TTT",
    "TTC",
    "GCA",
    "GCC",
    "GCG",
    "GCT",
    "GGT",
    "GGG",
    "GGA",
    "GGC",
    "ATC",
    "ATA",
    "ATT",
    "TTA",
    "TTG",
    "CTC",
    "CTT",
    "CTG",
    "CTA",
    "CAT",
    "CAC",
    "CGA",
    "CGC",
    "CGG",
    "CGT",
    "AGG",
    "AGA",
    "TGG",
    "GTA",
    "GTC",
    "GTG",
    "GTT",
    "GAG",
    "GAA",
    "TAT",
    "TAC",
}

EXCLUDE_CODONS: Final = {"ATG", "TGG"}
