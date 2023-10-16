__version__ = "0.1.0"

from . import (
    sequences,
    common,
    relations,
    taxonomy,
    virus_hosts,
    gc_content,
    codon,
    codon_pair,
    dinucleotides,
)
from Bio import Entrez
import os


def set_entrez_api_key(email: str = None, api_key: str = None):
    """Sets Entrez email and api key.

    The values are read from the ENV variables "ENTREZ_EMAIL" and "ENTREZ_API_KEY" if not explicitly given.

    For more information about the API, see
    https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen

    Parameters
    ----------
    email: str
        Email address of the NCBI account
    api_key : str
        API key of the NCBI account

    """
    if email is None:
        Entrez.email = os.environ["ENTREZ_EMAIL"]
    else:
        Entrez.email = email

    if api_key is None:
        Entrez.api_key = os.environ["ENTREZ_API_KEY"]
    else:
        Entrez.api_key = api_key
