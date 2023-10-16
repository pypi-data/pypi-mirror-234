"""Provides an easy method of getting taxonomic data from NCBIs taxonomy database and ICTVs metadata files.

Examples
--------
    >>> meta = seqhelp.taxonomy.get_ncbi_taxonomy("Homo sapiens")
    {'superkingdom': 'Eukaryota', 'realm': '', 'kingdom': 'Metazoa', 'phylum': 'Chordata', 'subphylum': 'Craniata', 'class': 'Mammalia', 'order': 'Primates', 'suborder': 'Haplorrhini', 'family': 'Hominidae', 'subfamily': 'Homininae', 'genus': 'Homo', 'subgenus': '', 'species': 'Homo sapiens', 'subspecies': '', 'strain': ''}

    >>> meta = seqhelp.taxonomy.get_ictv_taxonomy("Tobacco mosaic virus", "")
    defaultdict(<class 'str'>, {'realm': 'Riboviria', 'kingdom': nan, 'phylum': 'Negarnaviricota', 'subphylum': 'Haploviricotina', 'class': 'Chunqiuviricetes', 'order': 'Muvirales', 'suborder': nan, 'family': 'Qinviridae', 'subfamily': nan, 'genus': 'Yingvirus', 'subgenus': nan, 'species': 'Beihai yingvirus', 'genome composition': 'ssRNA(-)', 'host/source': 'invertebrates'})

"""

import functools
import logging
import os
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Final, Optional

import pandas as pd
from ete3 import NCBITaxa

Metadata = dict[str, dict[str, Any]]
Taxonomy = list[dict[str, str]]

SOUGHT_RANKS: Final = [
    "superkingdom",
    "realm",
    "kingdom",
    "phylum",
    "subphylum",
    "class",
    "order",
    "suborder",
    "family",
    "subfamily",
    "genus",
    "subgenus",
    "species",
    "subspecies",
    "strain",
]

ICTV_SOUGHT_RANK_NAMES: Final = [
    "Superkingdom",
    "Realm",
    "Kingdom",
    "Phylum",
    "Subphylum",
    "Class",
    "Order",
    "Suborder",
    "Family",
    "Subfamily",
    "Genus",
    "Subgenus",
    "Species",
    "Subspecies",
    "Strain",
    "Genome composition",
    "Host/Source",
]


@functools.lru_cache()
def parse_ictv(ictv_vmr_path: Path = None) -> Optional[pd.DataFrame]:
    if ictv_vmr_path is not None:
        return pd.read_excel(ictv_vmr_path)
    else:
        _ictv_vmr_dir = Path(os.path.realpath(__file__)).parent

        _ictv_vmr_path = next(
            (
                path
                for path in _ictv_vmr_dir.iterdir()
                if path.suffix == ".xlsx" and "VMR" in path.stem
            ),
            None,
        )
        if _ictv_vmr_path is not None:
            try:
                return pd.read_excel(_ictv_vmr_path)
            except FileNotFoundError as e:
                logging.debug("ICTV VMR not found in expected place.")

                _ictv_vmr_df = None
        else:
            url = "https://ictv.global/filebrowser/download/461"

            now = datetime.now().strftime("%Y-%m-%d")
            urllib.request.urlretrieve(url, _ictv_vmr_dir / f"VMR-{now}.xlsx")
            return parse_ictv()


def get_ictv_taxonomy(
    species: str, aid: str, ictv_vmr_path: Path = None
) -> Optional[dict[str, str]]:
    """Gets the taxonomy for the virus species from ictv.

    Parameters
    ----------
    species: str
        Species name
    aid: str
        Aid of sequence.
    ictv_vmr_path: Path
        Path to ictv vmr file.

    Returns
    -------
    taxonomy: Optional[Dict[str, str]]
        The taxonomic ranks for the species, as {"species": species, "family": family"} etc.

    """
    if species is None:
        return None

    ictv_vmr_df = parse_ictv(ictv_vmr_path)
    if ictv_vmr_df is None:
        raise FileNotFoundError("ICTV VMR not found")

    aid_ = aid.split(".")[0]
    df = ictv_vmr_df[
        (ictv_vmr_df["Species"] == species)
        | (ictv_vmr_df["Virus name(s)"] == species)
        | (ictv_vmr_df["Virus GENBANK accession"].str.contains(aid_))
        | (ictv_vmr_df["Virus REFSEQ accession"].str.contains(aid_))
    ]
    if len(df) == 0:
        logging.warning(f"Aid {aid} ({species}) not found in ICTV taxonomy")
        return None
    else:
        return defaultdict(
            str,
            {
                rank.lower(): df[rank].values[0]
                for rank in ICTV_SOUGHT_RANK_NAMES
                if rank in df.columns
            },
        )


@functools.lru_cache(128)
def get_ncbi_taxonomy(species: str) -> Optional[dict[str, str]]:
    """Gets the taxonomy for the species from ncbi.

    Parameters
    ----------
    species: str
        Species name

    Returns
    -------
    taxonomy: Optional[Dict[str, str]]
        The taxonomic ranks for the species, as {"species": species, "family": family"} etc.

    """
    if species is None:
        return None

    ncbi = NCBITaxa()
    name_translator = ncbi.get_name_translator([species])
    tax = _get_single_name_taxonomy(species, name_translator, ncbi)
    if tax is None:
        return None
    else:
        return parse_taxonomy(tax)


def _get_single_name_taxonomy(
    species: str, name_translator: dict[str, str], ncbi: NCBITaxa
) -> Optional[Taxonomy]:
    if species not in name_translator:
        return None
    taxid = name_translator[species][0]
    lineage = ncbi.get_lineage(taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)
    return [{"Rank": ranks[k], "ScientificName": names[k]} for k in lineage]


def parse_taxonomy(taxonomy: Taxonomy) -> dict[str, str]:
    """Parse out relevant taxonomic classes from the raw taxonomy.

    Parameters
    ----------
    taxonomy : List[Dict[str, str]]
        Raw taxonomy, as retrieved from the Taxonomy db

    Returns
    -------
    Dict[str, str]
        Dictionary with the ranks (e.g. "superkingdom") as keys
    """
    if taxonomy is None:
        return defaultdict(str)

    parsed_tax = {
        tax["Rank"]: tax["ScientificName"]
        for tax in taxonomy
        if tax["Rank"] in SOUGHT_RANKS
    }

    return defaultdict(str, {rank: parsed_tax.get(rank, "") for rank in SOUGHT_RANKS})
