"""
Parses and provides an interface to retrieve known virus-host information from the virus-host db of https://www.genome.jp/.

Examples
--------
    >>> virus_hosts.get_virus_hosts([(12242, "Tobacco mosaic virus", "NC_001367.1")])
    {'Tobacco mosaic virus': {'Nicotiana tabacum'}}

    Multiple of the fields can be None, but their presence makes the parsing more reliable:
    >>> seqhelp.virus_hosts.get_virus_hosts([(12242, "Tobacco mosaic virus", "NC_001367.1"), (None, "Human herpesvirus 3", None)])
    {'Tobacco mosaic virus': {'Nicotiana tabacum'}, 'Human herpesvirus 3': {'Homo sapiens'}}


"""

import functools
import logging
from collections import defaultdict
from pathlib import Path
import urllib.request

import pandas as pd
import os
from typing import List, Dict, Tuple, Set


@functools.lru_cache()
def _get_virus_host_db(path: str = None):
    if path is None:
        _virus_host_db_path = (
            Path(os.path.realpath(__file__)).parent / "virushostdb.tsv"
        )
        path = _virus_host_db_path

    if not Path(path).is_file():
        url = "https://www.genome.jp/ftp/db/virushostdb/virushostdb.tsv"

        logging.info(f"virushostdb not found, trying to fetch from {url}")

        urllib.request.urlretrieve(url, path)

    return _parse_virus_host_db(path)


@functools.lru_cache()
def _parse_virus_host_db(path: str):
    hosts_df = pd.read_csv(path, sep="\t")
    return hosts_df


def get_virus_hosts(
    tax_ids: List[Tuple[int, str, str]],
    path: str = None,
) -> Dict[str, Set[str]]:
    """Finds the virus hosts in a tab separated file by their tax id.

    The tsv file is from  ftp://ftp.genome.jp/pub/db/virushostdb/virushostdb.tsv

    Parameters
    ----------
    tax_ids : List[Tuple[int, str, str]]
        Taxa id, species and refseq id for each virus.
    path : str, optional
        Path to tsv file with viral host information
            Will be downloaded if not found.

    Returns
    -------
    dict
        Dictionary with species as key, and dictionary with metadata as value
        (with classes as key, e.g. "superkingdom", "gc_class")
    """

    hosts_df = _get_virus_host_db(path)

    return {
        species: set(
            host
            for host in _get_hosts(hosts_df, tax_id, species, refseq_aid)
            if str(host) != "nan"
        )
        for tax_id, species, refseq_aid in tax_ids
    }


def _get_hosts(hosts_df, tax_id: int, species: str, refseq_aid: str):
    if tax_id is None:
        tax_id_matches = []
    else:
        tax_id_matches = list(
            hosts_df[hosts_df["virus tax id"] == tax_id]["host name"].values
        )

    if species is None or species == "":
        species_matches = []
    else:
        species_matches = list(
            hosts_df[hosts_df["virus name"].str.contains(species, regex=False)][
                "host name"
            ].values
        ) + list(
            hosts_df[hosts_df["virus lineage"].str.contains(species, regex=False)][
                "host name"
            ].values
        )

    if refseq_aid is None or refseq_aid == "":
        refseq_matches = []
    else:
        refseq_aid = refseq_aid.split(".")[0]  # Don't care about version

        refseq_matches = list(
            hosts_df[hosts_df["refseq id"].str.contains(refseq_aid, regex=False)][
                "host name"
            ].values
        )

    return tax_id_matches + species_matches + refseq_matches


def get_host_names(tax_id: int, species: str, refseq_aid: str, path: str = None) -> List[str]:
    hosts_df = _get_virus_host_db(path)
    hosts = set(_get_hosts(hosts_df, tax_id, species, refseq_aid))
    return [name for name in hosts if str(name) != "nan"]
