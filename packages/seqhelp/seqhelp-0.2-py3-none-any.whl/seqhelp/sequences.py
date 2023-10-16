"""Provides a straight-forward approach to download and use genomic sequences, primarily from NCBI.

The main use-case is through the following functions:

- `get_sequence(aid, ...)` - returns a sequence matching the provided aid.
- `get_sequence_batch(aids, ...)` - returns an iterator with sequences matching the provided aids.

For additional convenience, the dustmasked, coding or non-coding version of the sequences can be requested.

Example
-------
    >>> rec = get_sequence("NC_001367.1", download_folder=Path.home() / "data")

"""

import enum
import functools
import gzip
import http.client
import http.client
import itertools
import json
import logging
import os
import re
import shutil
import subprocess
import urllib
from collections import defaultdict
from pathlib import Path
from typing import Optional, Tuple, Union
from collections.abc import Iterable, Iterator

import Bio
import numpy as np
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import tqdm


def get_or_download_fasta(
    aid: str, download_folder: Path, return_path: bool
) -> Optional[Bio.SeqRecord.SeqRecord | Path]:
    """Gets the fasta file for `aid` either in `download_folder` or by download it.

    Parameters
    ----------
    aid : str
        AID for entry to get fasta for
    download_folder : Path
        Path to directory where fasta files are saved
    return_path: bool
        True to get path, False to get SeqRecord

    Returns
    -------
    Union[Bio.SeqRecord, Path]
        Fasta file contents
    """

    path = get_path(aid, download_folder, [".fa", ".fasta", ".fna"])
    if path is None:
        with get_download_cache() as download_cache:
            if download_cache.has_full_failed(aid):
                return None

            logging.info(f"Found no fasta file for {aid}, attempting download.")
            try:
                fastas = list(get_fastas([aid]))
            except (
                urllib.error.HTTPError,
                http.client.IncompleteRead,
                ValueError,
            ) as e:
                logging.info("Could not download fasta.")
                download_cache.mark_full_as_failed(aid)
                return None

            if fastas is None:
                logging.info("Could not download fasta.")
                return None

            path = download_folder / f"{aid}.fa.gz"
            with gzip.open(path, "wt") as f:
                for fasta in fastas:
                    f.write(fasta.format("fasta"))

    if return_path:
        return path
    else:
        if path.suffix == ".gz":
            with gzip.open(path, "rt") as f:
                return next(SeqIO.parse(f, "fasta"), None)
        else:
            if path.stat().st_size == 0:
                return None
            with path.open("r") as f:
                return next(SeqIO.parse(f, "fasta"))


class DownloadType(enum.Enum):
    Full = "Full"
    Coding = "Coding"


def batch_download(
    ids: list[str],
    download_folder: Path,
    batch_size: int,
    download_type: DownloadType = DownloadType.Full,
):
    if len(ids) == 0:
        return

    logging.info(f"Downloading {ids}, with {download_type}")

    n_batches = np.maximum(len(ids) // batch_size, 1)
    batches = np.array_split(ids, n_batches)

    with tqdm.tqdm(batches) as pbar:
        for batch in pbar:
            pbar.set_description(f"Downloading {batch}")

            try:
                fastas = get_fastas(batch, download_type)
                if fastas is None:
                    return

                suffix = ""
                if download_type == DownloadType.Coding:
                    suffix = "_cds"

                for fasta in fastas:
                    id_ = fasta.id
                    if download_type == DownloadType.Coding:
                        id_, _ = fasta.id.split("_cds_")
                        id_ = id_.replace("lcl|", "")

                    path = download_folder / f"{id_}{suffix}.fa.gz"
                    with gzip.open(path, "at") as f:
                        f.write(fasta.format("fasta"))
            except http.client.IncompleteRead as e:
                logging.warning(e)
                continue


def get_or_download_gb(aid: str, download_folder: Path) -> Optional[SeqRecord]:
    """Gets the genbank file for `aid` either in `download_folder` or by download it.

    Parameters
    ----------
    aid : str
        AID for the entry
    download_folder : Path
        Path to directory where genbank files are saved

    Returns
    -------
    Bio.SeqRecord
        Genbank file.
    """

    gbs = get(aid, download_folder, [".gb"], "genbank")
    if gbs is None:
        logging.info(f"Found no genbank file for {aid}, attempting download.")
        gbs = list(get_gbs([aid]))
        if len(gbs) == 0:
            logging.info("Could not download genbank file.")
            return None

        path = download_folder / f"{aid}.gb.gz"
        with open(path, "w") as f:
            f.write(gbs[0].format("genbank"))

    return gbs[0]


def get(
    aid: str, download_folder: Path, suffixes: list[str], format_name: str = ""
) -> Optional[list[SeqRecord]]:
    """Try to retrieve the file for the aid with a suffix in suffixes.

    Parameters
    ----------
    aid : str
        AID for entry to get file for.
    download_folder : Path
        Path to directory with downloaded files.
    suffixes : list[str]
        list of file endings for downloaded files,
         e.g. [".fa", ".fasta"] for fasta files.
    format_name : str, optional
        Name of format for passing to SeqIO.parse (default "")

    Returns
    -------
    Bio.SeqRecord
        File contents or None if no file found.
    """
    path = get_path(aid, download_folder, suffixes)
    if path is None or not path.is_file():
        return None

    if path.suffix == ".gz":
        try:
            with gzip.open(path, "rt") as f:
                return list(SeqIO.parse(f, format_name))
        except gzip.BadGzipFile as e:
            # TODO oops no compression?
            path_no_comp = path.with_suffix(".tmp")
            shutil.move(path, path_no_comp)
            with gzip.open(path, "wt") as f_out:
                with path_no_comp.open("r") as f_in:
                    f_out.write(f_in.read())
            with gzip.open(path, "rt") as f:
                return list(SeqIO.parse(f, format_name))

    else:
        with path.open("r") as f:
            if ".tax" == path.suffix:
                return json.load(f)
            else:
                return list(SeqIO.parse(f, format_name))


def get_path(aid: str, download_folder: Path, suffixes: list[str]) -> Optional[Path]:
    """Get path to file with `aid` in `download_folder` and suffix in `suffixes`.

    Parameters
    ----------
    aid : str
        Accession id
    download_folder: Path
        Folder/directory where downloads are stored
    suffixes : list[str]
        Possible suffixes for this type of file.

    Returns
    -------
    Path
    """
    download_folder = Path(download_folder)

    # Add compression suffixes
    suffixes = suffixes + [f"{suf}.gz" for suf in suffixes]

    has_version_number = len(aid.split(".")) == 2
    if has_version_number:
        aids = [aid]
    else:
        aids = itertools.chain([aid], (f"{aid}.{i}" for i in reversed(range(50))))

    for aid_ in aids:
        for suffix in suffixes:
            path = download_folder / f"{aid_}{suffix}"

            if path.is_file():
                if path.suffix == ".gz":
                    return path
                else:
                    with gzip.open(f"{path}.gz", "wt") as f_out:
                        with path.open("r") as f_in:
                            f_out.write(f_in.read())
                    path.unlink()
                    return Path(f"{path}.gz")

    return None


class SequencePart(enum.Enum):
    Full = "Full"
    Coding = "Coding"
    NonCoding = "NonCoding"
    DustMasked = "DustMasked"
    TandemRepeatsFinder = "TandemRepeatsFinder"
    Genes = "Genes"


def _get_sequences(p: Path) -> list[SeqRecord]:
    with gzip.open(p, "rt") as f:
        return list(SeqIO.parse(f, "fasta"))


def _get_sequence(p: Path) -> SeqRecord:
    with gzip.open(p, "rt") as f:
        return SeqIO.read(f, "fasta")


def get_sequence_batch(
    aids: list[str],
    download_folder: Path = Path.home() / "data" / "downloads",
    sequence_part: SequencePart = SequencePart.Full,
    return_path: bool = False,
    batch_size: int = 50,
) -> Iterable[SeqRecord | Path]:
    """Retrieves the sequence with `aid` from `download_folder` or NCBI, in batches.

    Fetches the full sequence, coding, non-coding, or dustmasked sequence according to the `sequence_part` parameter.

    Parameters
    ----------
    aids : list[str]
        Accession ids from NCBi.
    download_folder : Path, optional
        Path to download folder where sequences are saved.  (defaults to "downloads").
    sequence_part : str, optional
        One of "Full", "Coding", "NonCoding", "RepeatMasked", "DustMasked".
    return_path : bool, optional
        False to get SeqRecord, True to get path to file
    batch_size: int, optional
        Number of records to download for each batch.  If the downloads fail frequently, lower the batch size.

    Returns
    -------
    Iterable[SeqRecord | Path]
        Iterable of SeqRecord of the sequence or paths.  Is empty if no sequence is found.

    Raises
    ------
    ValueError
        If sequence_part is not one of "Full", "Coding", "NonCoding", "DustMasked".

    """
    download_folder = Path(download_folder)

    if sequence_part not in SequencePart:
        allowed_values = ", ".join([part.name for part in SequencePart])
        raise ValueError(
            f"sequence_part is not a correct value ({sequence_part}). Should be one of {allowed_values}."
        )

    if sequence_part == SequencePart.Full:
        paths = [get_path(aid, download_folder, [".fa", ".fasta"]) for aid in aids]
        not_found_aids = [aid for aid, p in zip(aids, paths) if p is None]

        batch_download(not_found_aids, download_folder, batch_size, DownloadType.Full)
        all_paths = (get_path(aid, download_folder, [".fa", ".fasta"]) for aid in aids)
        if return_path:
            return all_paths
        else:
            return (_get_sequence(p) for p in all_paths)

    elif sequence_part == SequencePart.Coding:
        paths = [Path(download_folder / f"{aid}_joined_cds.fa.gz") for aid in aids]

        not_found_aids = [aid for aid, p in zip(aids, paths) if not p.is_file()]

        batch_download(not_found_aids, download_folder, batch_size, DownloadType.Coding)

        for aid in not_found_aids:
            try:
                join_cds(aid, download_folder)
            except ValueError as e:
                print(e)
                continue

        all_paths = [
            p
            for aid in aids
            if (p := Path(download_folder / f"{aid}_joined_cds.fa.gz")).is_file()
        ]

        if return_path:
            return all_paths
        else:
            return (_get_sequences(p) for p in all_paths)

    elif sequence_part == SequencePart.Genes:
        paths = [Path(download_folder / f"{aid}_cds.fa.gz") for aid in aids]

        not_found_aids = [aid for aid, p in zip(aids, paths) if not p.is_file()]

        batch_download(not_found_aids, download_folder, batch_size, DownloadType.Coding)

        working_paths = [p for p in paths if p.is_file()]

        if return_path:
            return working_paths
        else:
            return (_get_sequences(p) for p in working_paths)

    elif sequence_part == SequencePart.NonCoding:
        return [non_coding_sequence(aid, download_folder, return_path) for aid in aids]

    elif sequence_part == SequencePart.DustMasked:
        paths = [
            get_path(
                aid,
                download_folder,
                [".fa.dustmasked", ".fasta.dustmasked"],
            )
            for aid in aids
        ]
        not_found_aids = [aid for aid, p in zip(aids, paths) if p is None]

        batch_download(not_found_aids, download_folder, batch_size, DownloadType.Full)

        for path, aid in zip(paths, aids):
            # If we had to download it, it also needs dustmasking
            if path is None:
                record = get_or_download_fasta(aid, download_folder, return_path=False)
                if record is None:
                    continue
                dustmasked = dustmask_record(record)
                path = download_folder / f"{aid}.fa.dustmasked"
                SeqIO.write(dustmasked, path, "fasta")

        working_paths = [p for p in paths if p is not None and p.is_file()]

        if return_path:
            return working_paths
        else:
            return (_get_sequence(p) for p in working_paths)

    elif sequence_part == SequencePart.TandemRepeatsFinder:
        paths = [
            get_path(
                aid,
                download_folder,
                [".fa.2.7.7.80.10.50.500.mask", ".fasta.2.7.7.80.10.50.500.mask"],
            )
            for aid in aids
        ]
        for path, aid in zip(paths, aids):
            if path is None:
                record = get_or_download_fasta(aid, download_folder)
                repeat_masked = tandem_repeats_finder(
                    record, aid, download_folder
                )  # This stores the fasta automatically

                path = get_path(
                    aid,
                    download_folder,
                    [".fa.2.7.7.80.10.50.500.mask", ".fasta.2.7.7.80.10.50.500.mask"],
                )

    if return_path:
        return paths
    else:
        sequences = [SeqIO.parse(path, format="fasta") for path in paths]
        return [SeqRecord(seq=sequence.seq, id=aid, name=aid) for sequence in sequences]


def get_sequence(
    aid: str,
    download_folder: Path = Path.home() / "data" / "downloads",
    sequence_part: SequencePart = SequencePart.Full,
    return_path: bool = False,
) -> Optional[SeqRecord | Path]:
    """Retrieve the sequence with `aid` from `download_folder` or GenBank.

    Fetches the full sequence, coding, non-coding, or dustmasked sequence according to the `sequence_part` parameter.

    Parameters
    ----------
    aid : str
        Accession id from GenBank.
    download_folder : Path, optional
        Path to download folder where sequences are saved.  (defaults to "downloads").
    sequence_part : str, optional
        One of "Full", "Coding", "NonCoding", "RepeatMasked", "DustMasked".
    return_path : bool, optional
        False to get SeqRecord, True to get path to file

    Returns
    -------
    Optional[SeqRecord]
        SeqRecord of the sequence, or None if no sequence is found.

    Raises
    ------
    ValueError
        If sequence_part is not one of "Full", "Coding", "NonCoding", "DustMasked".

    """
    if sequence_part == SequencePart.Full:
        return get_or_download_fasta(aid, download_folder, return_path)
    elif sequence_part == SequencePart.Genes:
        path = Path(download_folder / f"{aid}_cds.fa.gz")

        if not path.is_file():
            # get_or_download_cds(aid, download_folder)
            batch_download([aid], download_folder, 1, DownloadType.Coding)

        if return_path:
            return path
        else:
            return _read_fasta(path)[0]

    elif sequence_part == SequencePart.Coding:
        return coding_sequence(aid, download_folder, return_path)
    elif sequence_part == SequencePart.NonCoding:
        return non_coding_sequence(aid, download_folder, return_path)
    elif sequence_part == SequencePart.DustMasked:
        path = get_path(
            aid,
            download_folder,
            [".fa.dustmasked", ".fasta.dustmasked"],
        )
        if path is None:
            record = get_or_download_fasta(aid, download_folder, return_path=False)
            if record is None:
                return None
            dustmasked = dustmask_record(record)
            path = download_folder / f"{aid}.fa.dustmasked.gz"
            with gzip.open(path, "wt") as f:
                SeqIO.write(dustmasked, f, "fasta")

    elif sequence_part == SequencePart.TandemRepeatsFinder:
        path = get_path(
            aid,
            download_folder,
            [".fa.2.7.7.80.10.50.500.mask", ".fasta.2.7.7.80.10.50.500.mask"],
        )
        if path is None:
            record = get_or_download_fasta(aid, download_folder, return_path=False)
            _ = tandem_repeats_finder(
                record, aid, download_folder
            )  # This stores the fasta automatically

            path = get_path(
                aid,
                download_folder,
                [".fa.2.7.7.80.10.50.500.mask", ".fasta.2.7.7.80.10.50.500.mask"],
            )
    else:
        allowed_values = ", ".join([part.name for part in SequencePart])
        raise ValueError(
            f"sequence_part is not a correct value ({sequence_part}). Should be one of {allowed_values}."
        )

    if return_path:
        return path
    else:
        sequences = _read_fasta(path)
        return SeqRecord(seq=sequences[0].seq, id=aid, name=aid)


def _read_fasta(path: Path) -> list[SeqRecord]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt") as f:
            sequences = list(SeqIO.parse(f, format="fasta"))
    else:
        with path.open("r") as f:
            sequences = list(SeqIO.parse(f, format="fasta"))
    return sequences


def get_cds_path(aid: str, download_folder: Path) -> Optional[Path]:
    """Get path to CDS.

    Parameters
    ----------
    aid : str
        Accession id in GenBank.
    download_folder : Path
        Path to where cds is saved.

    Returns
    -------
    Optional[Path]
        Path to CDS file.
    """
    download_folder = Path(download_folder)
    file_name = f"{aid}_cds"
    cds_path = get_path(file_name, download_folder, [".fa", ".fasta"])
    return cds_path


def get_or_download_cds(
    aid: str, download_folder: Path, return_path: bool = False
) -> Optional[list[SeqRecord] | Path]:
    """Downloads or fetches coding sequence wth `aid` from GenBank.

    Parameters
    ----------
    aid: str
        Accession id in GenBank
    download_folder: str
        Path to where to save the sequence.
    return_path: bool
        Flag for returning SeqRecord or Path to SeqRecord

    Returns
    -------
    Optional[list[SeqRecord]]
        list of SeqRecord of coding sequences.
    """

    file_name = f"{aid}_cds"

    path = get_path(file_name, download_folder, [".fa", ".fasta"])

    if path is not None and return_path:
        return path

    cds = get(file_name, download_folder, [".fa", ".fasta"], "fasta")

    if cds is None:
        term = f'"{aid}"[Accession]'
        search_handle = Entrez.esearch(
            db="Nucleotide", retmax=1, term=term, idtype="acc"
        )
        search_record = Entrez.read(search_handle)
        ids = search_record.get("Idlist", search_record.get("IdList", []))

        cds_handles = Entrez.efetch(
            db="Nucleotide", id=ids, rettype="fasta_cds_na", retmode="text"
        )
        cds = list(SeqIO.parse(cds_handles, "fasta"))

        path = download_folder / f"{file_name}.fa.gz"
        with gzip.open(path, "wt") as f:
            SeqIO.write(cds, f, "fasta")

    if return_path:
        return path
    else:
        return cds


def get_gbs(ids: list[str]) -> Iterator[SeqRecord]:
    """Get the corresponding genbank files from genbank.

    Uses Entrez to find the correct matches.

    Parameters
    ----------
    ids : list[str]
        list of ids to search for.

    Returns
    -------
    Iterator[SeqRecord]
        The corresponding genbank records.
    """
    try:
        gb_handles = Entrez.efetch(
            db="Nucleotide", id=ids, rettype="gb", retmode="text"
        )

        for gb in SeqIO.parse(gb_handles, "genbank"):
            yield gb
    except (
        http.client.IncompleteRead,
        urllib.error.HTTPError,
        ConnectionResetError,
        RuntimeError,
    ) as e:
        logging.warning(f"Some of ids {ids} could not be downloaded, with {e}.")
        return


def get_fastas(
    ids: list[str], download_type: DownloadType = DownloadType.Full
) -> Iterator[SeqRecord]:
    """Get the corresponding fasta files from genbank.

    Uses Entrez to find the correct matches.

    Parameters
    ----------
    ids : list[str]
        list of ids to search for.
    download_type: DownloadType
        Type of download, either DownloadType.Full or DownloadType.Coding.

    Returns
    -------
    Iterator[SeqRecord]
        The corresponding fasta records.
    """
    term = " OR ".join([f'"{id_}"[Accession]' for id_ in ids])
    search_handle = Entrez.esearch(
        db="Nucleotide", retmax=6000, term=term, idtype="acc"
    )
    search_record = Entrez.read(search_handle)
    ids = search_record.get("Idlist", search_record.get("IdList", []))

    if download_type == DownloadType.Full:
        rettype = "fasta"
    elif download_type == DownloadType.Coding:
        rettype = "fasta_cds_na"
    else:
        raise ValueError(f"Download type {download_type} is invalid")

    try:
        fasta_handles = Entrez.efetch(
            db="Nucleotide", id=ids, rettype=rettype, retmode="text"
        )
    except (
        http.client.IncompleteRead,
        urllib.error.HTTPError,
        ConnectionResetError,
        RuntimeError,
    ) as e:
        logging.warning(f"Some of ids {ids} could not be downloaded, with {e}.")
        return None

    return SeqIO.parse(fasta_handles, "fasta")


def coding_sequence(
    aid: str, download_folder: Path, return_path: bool
) -> Optional[SeqRecord | Path]:
    """Get the coding sequence for the aid.

    Joins individual genes with "NNN" to preserve the frame

    Parameters
    ----------
    aid : str
        Accession id for the sequence.
    download_folder : Path
        Path to downloaded files.
    return_path : bool, optional
        False to get SeqRecord, True to get path to file

    Returns
    -------
    Union[SeqRecord, Path]
        SeqRecord of the coding sequence, or path.
    """
    path_no_comp = Path(download_folder / f"{aid}_joined_cds.fa")
    path = Path(f"{path_no_comp}.gz")
    if path_no_comp.is_file():
        with gzip.open(path, "wt") as f_out:
            with path_no_comp.open("r") as f_in:
                f_out.write(f_in.read())
        path_no_comp.unlink()

    if path.is_file() and return_path:
        # TODO remove once the fuckup is resolved
        try:
            with gzip.open(path, "rt") as f:
                f.readline()
        except gzip.BadGzipFile:
            shutil.move(path, path_no_comp)
            with gzip.open(path, "wt") as f_out:
                with path_no_comp.open("r") as f_in:
                    f_out.write(f_in.read())
        return path
    elif path.is_file():
        with gzip.open(path, "rt") as f:
            return SeqIO.read(f, "fasta")

    with get_download_cache() as download_cache:
        if download_cache.has_coding_failed(aid):
            return None
        try:
            cds: list[SeqRecord] = list(get_or_download_cds(aid, download_folder))
        except (urllib.error.HTTPError, http.client.IncompleteRead, ValueError) as e:
            logging.warning(
                f"Coding sequence of {aid} could not be downloaded, with {e}."
            )
            download_cache.mark_coding_as_failed(aid)
            return None

    record = _join_cds(aid, cds, path)

    if return_path and record is not None:
        return path
    else:
        return record


def join_cds(aid: str, download_folder: Path):
    joined_cds_path = Path(download_folder / f"{aid}_joined_cds.fa.gz")

    if joined_cds_path.is_file():
        return

    raw_cds_path = Path(download_folder / f"{aid}_cds.fa")
    if not raw_cds_path.is_file():
        raise ValueError(f"The cds of {aid} is not downloaded.")

    cds = list(SeqIO.parse(raw_cds_path, "fasta"))
    _join_cds(aid, cds, joined_cds_path)

    return joined_cds_path


def _join_cds(aid: str, cds: list[SeqRecord], path: Path) -> Optional[SeqRecord]:
    gene_records = join_records_by_gene(cds, aid)

    if len(gene_records) == 0:
        return None

    sequence = "NNN".join(str(region.seq) for region in gene_records)
    record = SeqRecord(Seq(sequence), id=aid)

    if path.suffix == ".gz":
        with gzip.open(path, "wt") as f:
            f.write(record.format("fasta"))
    else:
        with path.open("w") as f:
            f.write(record.format("fasta"))

    return record


def join_records_by_gene(records: list[SeqRecord], aid: str) -> list[SeqRecord]:
    """Groups the records by their gene (as defined in the description), and joins their sequences.

    Parameters
    ----------
    records: list[SeqRecord]
        The list of genes to join
    aid: str
        Identifier of the records

    Returns
    -------
    list[SeqRecords]
        Each gene is one entry, and each entry is the concatenation of the genes.

    """
    genes = group_records_by_gene(records)

    return [_join_records(gene_records, aid) for gene_records in genes]


def group_records_by_gene(records: list[SeqRecord]) -> list[list[SeqRecord]]:
    """Groups the records by their gene (as defined in the description).

    Parameters
    ----------
    records: list[SeqRecord]
        Records to group by gene.

    Returns
    -------
    list[list[SeqRecord]]
        list of list with the records for each gene.
    """
    genes = defaultdict(list)
    for record in records:
        genes[_parse_gene(record)].append(record)

    return list(genes.values())


def _join_records(records: list[SeqRecord], aid: str) -> SeqRecord:
    sequence = "".join([str(record.seq) for record in records])
    joined_record = SeqRecord(Seq(sequence))
    joined_record.id = aid + "_" + _parse_gene(records[0])
    return joined_record


def non_coding_sequence(
    aid: str, download_folder: Path, return_path: bool
) -> Optional[SeqRecord | Path]:
    """Get the non-coding sequence for the aid.

    Parameters
    ----------
    aid : str
        Accession id for the sequence.
    download_folder : Path
        Path to downloaded files.
    return_path : bool, optional
        False to get SeqRecord, True to get path to file

    Returns
    -------
    SeqRecord | Path
        SeqRecord of the non-coding sequence, or path.
    """
    cds = get_or_download_cds(aid, download_folder)
    if cds is None:
        return None

    fasta = get_or_download_fasta(aid, download_folder, return_path)

    if fasta is None or cds is None:
        return None

    records = get_non_coding_segments(fasta, cds)

    combined_sequence = "NNN".join([str(rec.seq) for rec in records])
    record = SeqRecord(Seq(combined_sequence), id=aid)

    path = Path(download_folder / f"{aid}_non_coding.fa")
    with path.open("w") as f:
        f.write(record[0].format("fasta"))

    if return_path:
        return path
    else:
        return record


def get_non_coding_segment_bounds_aid(
    aid: str, download_folder: Path
) -> list[tuple[int, int]]:
    """Get the segment bounds (start and end index) from the sequence with `aid`.

    Parameters
    ----------
    aid : str
        Aid of seqrecord in ncbi
    download_folder: Path
        Where sequences are stored on disk

    Returns
    -------
    list[tuple[int, int]]
        list of bounds of non-coding segments

    """
    sequence = get_or_download_fasta(aid, download_folder, return_path=False)
    cds = get_or_download_cds(aid, download_folder)
    return get_non_coding_segment_bounds(sequence, cds)


def get_non_coding_segment_bounds(
    sequence: SeqRecord, cds: list[SeqRecord]
) -> list[tuple[int, int]]:
    """Get the segment bounds (start and end index) in sequence that is not referenced as coding in the cds.

    Parameters
    ----------
    sequence : SeqRecord
        Full sequence
    cds : list[SeqRecord]
        list of coding sequence records

    Returns
    -------
    list[tuple[int, int]]
        list of non-coding segments

    """
    sequence = str(sequence.seq)

    starts = []
    ends = []
    for region in cds:
        region_starts, region_ends = _get_coding_region_bounds(region)

        starts.extend(region_starts)
        ends.extend(region_ends)

    starts, ends = _merge_overlapping_regions(starts, ends)

    def bounds():
        last_end = 0
        for start, end in zip(starts, ends):
            if start - last_end > 0:
                yield last_end, start
            last_end = end + 1
        yield last_end, len(sequence)

    non_coding_sequences = [(start, end) for start, end in bounds()]

    return non_coding_sequences


def get_non_coding_segments(
    sequence: SeqRecord, cds: list[SeqRecord]
) -> list[SeqRecord]:
    """Get the segments in sequence that is not referenced as coding in the cds.

    Parameters
    ----------
    sequence : SeqRecord
        Full sequence
    cds : list[SeqRecord]
        list of coding sequence records

    Returns
    -------
    list[SeqRecord]
        list of non-coding segments

    """
    bounds = get_non_coding_segment_bounds(sequence, cds)

    non_coding_sequences = [
        SeqRecord(
            Seq(sequence[start:end]),
            id=f"non_coding_{start}-{end}",
            description=f"[locus_tag=non_coding_{start}_{end}]",
        )
        for start, end in bounds
    ]

    return non_coding_sequences


def _merge_overlapping_regions(
    starts: list[int], ends: list[int]
) -> Tuple[list[int], list[int]]:
    merged_starts = []
    merged_ends = []
    for start, end in zip(sorted(starts), sorted(ends)):
        if len(merged_ends) == 0 or start > merged_ends[-1]:
            merged_starts.append(start)
            merged_ends.append(end)
        else:
            merged_ends[-1] = end

    return merged_starts, merged_ends


def _get_coding_region_bounds(region: SeqRecord) -> tuple[list[int], list[int]]:
    starts = []
    ends = []

    # I'm sure there's an easier way to find this information somehow.
    pattern = (
        r"location=[(join)|(complement)\(]*"
        r"(?P<joins>([<>]?[0-9]+[<>]?(\.\.[<>]?[0-9]+[<>]?)?,?)+)\)?"
    )
    m = re.search(pattern, region.description)
    if m is not None:
        groupdict = m.groupdict()
        bounds = groupdict["joins"].split(",")
        for bound in bounds:
            if ".." in bound:
                start, end = bound.split("..")
            else:
                start, end = bound, bound

            starts.append(int(start.replace("<", "").replace(">", "")))
            ends.append(int(end.replace("<", "").replace(">", "")))

    return starts, ends


def _parse_gene(region: SeqRecord) -> str:
    pattern = r"((gene)|(locus_tag))=(?P<gene>[a-zA-Z0-9_]+)"
    m = re.search(pattern, region.description)
    if m is not None:
        groupdict = m.groupdict()
        return groupdict["gene"]
    else:
        return ""


def tandem_repeats_finder(
    record: SeqRecord, aid: str, download_folder: Path
) -> Optional[SeqRecord]:
    """Runs tandem repeats finder on the SeqRecord

    Parameters
    ----------
    record: SeqRecord
        Record to run tandem repeats finder on
    aid: str
        Aid of the record
    download_folder: Path
        Path to where the result and record is stored

    Returns
    -------
    SeqRecord
        Repeat masked sequence
    """
    trf_parameters = ("2", "7", "7", "80", "10", "50", "500", "-f", "-d", "-h", "-m")

    masked_extra_suffix = "2.7.7.80.10.50.500.mask"
    suffixes = ["fasta", "fa"]

    if not any(
        (Path(download_folder) / f"{aid}.{suffix}").is_file() for suffix in suffixes
    ):
        # None of the suffixes worked, so need to write file first.
        p = Path(download_folder) / f"{aid}.fasta"
        SeqIO.write(record, p, "fasta")

    for suffix in suffixes:
        p = Path(download_folder) / f"{aid}.{suffix}"
        if p.is_file():
            args = ("trf", str(p), *trf_parameters)
            res = subprocess.run(args, capture_output=True, cwd=download_folder)
            if res.returncode != 0:
                logging.warning("Tandem Repeats Masker did not work")
                logging.warning(f"Error message: {res.stderr}")

            masked_p = f"{p}.{masked_extra_suffix}"
            rec = SeqIO.read(masked_p, "fasta")
            return rec

    return None


def dustmask_record(record: SeqRecord) -> SeqRecord:
    """Runs dustmasker as on the SeqRecord.

    The dustmasker program has to be installed on the system, and is run as a subprocess.  Can be found on ubuntu
    in the ncbi-tools package.

    Parameters
    ----------
    record: SeqRecord
        Records to dustmask

    Returns
    -------
    SeqRecord
        The `record` with sequence updated as the dustmasked sequence.

    """

    logging.info(f"Running dustmasker on {record.id}")
    args = "/usr/bin/dustmasker -in -".split(" ")
    completed = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        input=record.format("fasta").encode(),
    )
    output = completed.stdout.decode()

    intervals = [
        _parse_interval(line)
        for line in output.split("\n")
        if len(line) > 0 and line[0] != ">"
    ]

    if len(intervals) == 0:
        return record

    sequence = ""
    prev_end = 0
    for start, end in intervals:
        sequence += str(record.seq[prev_end:start]) + "N" * (end - start)
        prev_end = end

    sequence += str(record.seq[prev_end : len(record.seq)])

    new_record = SeqRecord(record)
    new_record.seq = Seq(sequence)
    new_record.id = record.id

    return new_record


def _parse_interval(line: str) -> Tuple[int, int]:
    [start, end] = line.split(" - ")
    return int(start), int(end)


class DownloadCache:
    DOWNLOAD_STATUS_CACHE_PATH: Path = (
        Path.home() / "cache" / "seqhelp" / "download-status.json"
    )
    DOWNLOAD_STATUS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

    _cache = dict()

    def __init__(self):
        if self.DOWNLOAD_STATUS_CACHE_PATH.is_file():
            try:
                with self.DOWNLOAD_STATUS_CACHE_PATH.open("r") as f:
                    self._cache = json.load(f)
            except json.decoder.JSONDecodeError as e:
                logging.info(f"Failed to load download cache status with {e}")
                self._cache = dict()
        else:
            self._cache = dict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.DOWNLOAD_STATUS_CACHE_PATH.open("w") as f:
            json.dump(self._cache, f)

    def __getitem__(self, item):
        if item in self._cache:
            return self._cache[item]

    def __setitem__(self, key, value):
        self._cache[key] = value

    def mark_coding_as_failed(self, key):
        if key not in self._cache:
            self._cache[key] = dict()

        self._cache[key]["coding"] = False

    def mark_full_as_failed(self, key):
        if key not in self._cache:
            self._cache[key] = dict()

        self._cache[key]["full"] = False

    def has_coding_failed(self, key):
        if key in self._cache and "coding" in self._cache[key]:
            return True
        else:
            return False

    def has_full_failed(self, key):
        if key in self._cache and "full" in self._cache[key]:
            return True
        else:
            return False


@functools.cache
def get_download_cache():
    return DownloadCache()


def _adjacent_ns(left: str, right: str) -> bool:
    return left == "N" and right == "N"


def compress_ns(record: SeqRecord) -> SeqRecord:
    """
    Compresses adjacent N characters in the SeqRecord.
    Parameters
    ----------
    record: SeqRecord from biopython to compress

    Returns
    -------
    SeqRecord with compressed Ns
    """
    sequence = compress_ns_str(str(record.seq))

    new_record = SeqRecord(record)
    new_record.seq = Seq(sequence)
    new_record.id = record.id
    return new_record


def compress_ns_str(sequence: str) -> str:
    """
    Compresses adjacent N characters in the str.
    Parameters
    ----------
    sequence: str to compress

    Returns
    -------
    SeqRecord with compressed Ns
    """
    sequence = "".join(
        [s for s, sn in zip(sequence, sequence[1:]) if not _adjacent_ns(s, sn)]
        + [sequence[-1]]
    )

    return sequence
