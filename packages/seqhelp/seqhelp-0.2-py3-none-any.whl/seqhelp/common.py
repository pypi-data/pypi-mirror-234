import functools
import gzip
import itertools
import json
import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Final, Iterable, List, Optional, Tuple

import numba
import numpy as np
from Bio import SeqIO, SeqUtils
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from . import sequences, taxonomy, virus_hosts
from .taxonomy import Metadata

RANKS: Final[List[str]] = [
    "species",
    "genus",
    "family",
    "order",
    "class",
    "phylum",
    "kingdom",
    "superkingdom",
]

ranks_and_none = RANKS + ["None"]


if "DOWNLOAD_ROOT" in os.environ:
    DOWNLOAD_ROOT: Final[Path] = Path(os.environ["DOWNLOAD_ROOT"])
else:
    DOWNLOAD_ROOT: Final[Path] = Path.home() / "data" / "ftp.ncbi.nlm.nih.gov"

if "DOWNLOAD_FOLDER" in os.environ:
    DOWNLOAD_FOLDER: Final[Path] = Path(os.environ["DOWNLOAD_FOLDER"])
else:
    DOWNLOAD_FOLDER: Final[Path] = Path.home() / "data" / "downloads"

if "VIRUSLIST" in os.environ:
    virus_list_path: Final[Path] = Path(os.environ["VIRUSLIST"])
else:
    virus_list_path: Final[Path] = None


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


@functools.lru_cache()
def get_directory(name: str):
    now = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path("..") / "results" / name / now
    out_dir.mkdir(exist_ok=True, parents=True)
    return out_dir


def get_hosts() -> List[Dict[str, str]]:
    assemblies_path: Final[Path] = (
        Path(os.path.realpath(__file__)).parent.parent / "assembly_ids.json"
    )

    with assemblies_path.open("r") as f:
        hosts: List[Dict[str, str]] = json.load(f)

    hosts = [organism for organism in hosts if organism["aid"] != ""]
    unique_hosts = list({organism["aid"]: organism for organism in hosts}.values())

    return hosts


def to_fs_path(ftp_path: str, sequence_part: str = "coding") -> Optional[Path]:
    if sequence_part not in ["coding", "full-genome"]:
        raise ValueError("sequence_part has invalid value")

    path = DOWNLOAD_ROOT / Path(ftp_path)
    if not path.is_dir():
        logging.debug(f"{path} not found")
        return None

    version_path = next(path.iterdir())
    file_path = next(
        (path for path in version_path.iterdir() if _valid_path(path, sequence_part)),
        None,
    )
    return file_path


def _valid_path(path: Path, sequence_part: str) -> bool:
    if sequence_part == "coding":
        return "cds" in path.name
    else:
        return True


def parse_to_ftp_paths(hosts: List[Dict[str, Any]]) -> List[str]:
    return [to_ftp_path(organism["aid"]) for organism in hosts]


def to_ftp_path(aid: str, root: str = "genomes/all") -> str:
    db, number_and_version = aid.split("_")
    number, version = number_and_version.split(".")
    return f"{root}/{db}/{number[0:3]}/{number[3:6]}/{number[6:9]}"


def get_viruses() -> List[str]:
    virus_path = virus_list_path
    if virus_path is None or not virus_path.is_file():
        virus_path_ = Path.cwd().parent / "viruslist.txt"
        if virus_path_.is_file():
            virus_path = virus_path_

    viruses = virus_path.open("r").read().splitlines()
    return viruses


mononegavirales = [
    "Artoviridae",
    "Bornaviridae",
    "Filoviridae",
    "Lispiviridae",
    "Mymonaviridae",
    "Nyamiviridae",
    "Paramyxoviridae",
    "Pneumoviridae",
    "Rhabdoviridae",
    "Sunviridae",
    "Xinmoviridae",
]


def get_virus_hosts(virus_metadata: Metadata) -> Dict[str, List[Dict[str, str]]]:
    logging.info("Getting Hosts...")

    hosts_path = (
        Path(os.path.realpath(__file__)).parent.parent.parent
        / "cache"
        / "virus_hosts.json"
    )

    if hosts_path.exists():
        return json.load(hosts_path.open("r"))

    tax_ids = [
        (-1, t.get("species", None), t.get("aid", None))
        for t in virus_metadata.values()
    ]

    hosts = virus_hosts.get_virus_hosts(tax_ids)
    hosts = {
        key: [
            val
            for val in [taxonomy.get_ncbi_taxonomy(h) for h in hs]
            if val is not None
        ]
        for key, hs in hosts.items()
    }

    json.dump(hosts, hosts_path.open("w"))

    return hosts


def virus_row(aid: str, virus_metadata: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    return {
        "aid": aid,
        "virus": virus_metadata[aid]["species"],
        "species": virus_metadata[aid]["species"],
        "virus_genus": virus_metadata[aid]["genus"],
        "genus": virus_metadata[aid]["genus"],
        "virus_family": virus_metadata[aid]["family"],
        "family": virus_metadata[aid]["family"],
        "virus_order": virus_metadata[aid]["order"],
        "baltimore": virus_metadata[aid]["genome composition"],
        "sequence_length": _sequence_length(aid),
        "log_sequence_length": np.log10(_sequence_length(aid)),
        "average_gc_content": _gc_content(aid),
        "host_group": virus_metadata[aid]["host/source"],
    }


def _sequence_length(aid: str) -> int:
    record = sequences.get_sequence(
        aid, DOWNLOAD_FOLDER, sequences.SequencePart.DustMasked
    )
    if record is None:
        return 0
    else:
        return len(record.seq)


def _gc_content(aid: str) -> int:
    record = sequences.get_sequence(
        aid, DOWNLOAD_FOLDER, sequences.SequencePart.DustMasked
    )
    if record is None:
        return 0
    else:
        return SeqUtils.GC(record.seq) / 100


def clean_name(name: str) -> str:
    return (
        str(name).replace("\\", "").replace("(", "").replace(")", "").replace("/", "")
    )


def parse_genome_composition(composition: str) -> Tuple[str, str, str]:
    return (
        _parse_genome(composition),
        _parse_type(composition),
        _parse_sense(composition),
    )


def _parse_genome(composition: str) -> str:
    if "DNA" in composition:
        return "DNA"
    elif "RNA" in composition:
        return "RNA"
    else:
        return ""


def _parse_type(composition: str) -> str:
    if "ss" in composition:
        type_ = "single-stranded"
    elif "ds" in composition:
        type_ = "double-stranded"
    else:
        type_ = ""

    if "RT" in composition:
        type_ = type_ + "-RT"

    return type_


def _parse_sense(composition: str) -> str:
    if "+" in composition and "-" in composition:
        return "+/-"
    elif "+" in composition:
        return "+"
    elif "-" in composition:
        return "-"
    else:
        return ""


@functools.lru_cache()
def get_host_aids():
    hosts = get_hosts()

    return [h["aid"] for h in hosts]


@functools.lru_cache()
def get_host_metadata():
    logging.info("Getting metadata...")
    metadata_path = (
        Path(os.path.realpath(__file__)).parent.parent.parent
        / "cache"
        / "host_metadata.json"
    )

    if metadata_path.exists():
        return {
            key: defaultdict(str, value)
            for key, value in json.load(metadata_path.open("r")).items()
        }

    hosts = get_hosts()
    ftp_paths = parse_to_ftp_paths(hosts)

    file_paths = [to_fs_path(path, "coding") for path in ftp_paths]

    records = (
        (_join_sequences(path, host["aid"]), host)
        for path, host in zip(file_paths, hosts)
    )

    metadata = {
        host["aid"]: _host_meta(host["aid"], seq, host["species"])
        for seq, host in records
    }

    json.dump(metadata, metadata_path.open("w"))

    return metadata


def _host_meta(aid: str, record: SeqRecord, species: str):
    sequence = str(record.seq)
    tax = taxonomy.get_ncbi_taxonomy(species)

    meta = {
        "model": "VLMC",
        "name": species,
        "species": species,
        "unique_id": aid,
        "sequence_length": len(sequence),
        "average_gc_content": SeqUtils.GC(sequence) / 100,
        "aid": aid,
    }

    if tax is not None:
        meta = {**meta, **tax}

    return meta


def get_joined_host_coding_sequence() -> Iterable[tuple[SeqRecord, dict[str, str]]]:
    hosts = get_hosts()
    ftp_paths = parse_to_ftp_paths(hosts)

    file_paths = [to_fs_path(path, "coding") for path in ftp_paths]

    return (
        (_join_sequences(path, host["aid"]), host)
        for path, host in zip(file_paths, hosts)
        if path is not None and path.is_file()
    )


def _join_sequences(path: Path, aid: str) -> SeqRecord:
    if path is not None and path.is_file():
        records = SeqIO.parse(gzip.open(path, "rt"), "fasta")
        sequence = "N".join(str(record.seq) for record in records)
        return SeqRecord(Seq(sequence), id=aid)
    else:
        return SeqRecord(Seq(""), id=aid)


@numba.njit
def cosine_distance(left: np.ndarray, right: np.ndarray) -> float:
    denom = np.linalg.norm(left) * np.linalg.norm(right)
    if denom == 0:
        return np.nan

    correlation = np.minimum(1.0, np.sum(left * right) / denom)

    return 2 * np.arccos(correlation) / np.pi


def cosine_distances(lefts: np.ndarray, rights: np.ndarray = None) -> np.ndarray:
    if rights is None:
        rights = lefts
    return _cosine_distances(lefts, rights)


@numba.njit(parallel=True)
def _cosine_distances(lefts: np.ndarray, rights: np.ndarray) -> np.ndarray:
    matrix = np.zeros((len(lefts), len(rights)))
    for i in numba.prange(len(lefts)):
        for j in range(len(rights)):
            matrix[i, j] = cosine_distance(lefts[i], rights[j])

    return matrix
