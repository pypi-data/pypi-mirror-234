import functools
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from . import common
from .common import RANKS


@dataclass(frozen=True)
class Relations:
    signatures: tuple
    metadata: Dict[str, Dict[str, Any]]
    virus_hosts: Dict[str, List[Dict[str, str]]]
    hosts: bool
    unique_id: int = field(default_factory=uuid.uuid4)

    def __hash__(self):
        # This isn't important, needed only to allow for caching of the results
        return hash(self.unique_id)

    @functools.lru_cache()
    def index_of_clade_relations(self, virus: str, rank: str) -> Set[int]:
        virus_species = self.metadata[virus]["species"]

        if self.hosts:
            return set(
                i
                for (i, sig) in enumerate(self.signatures)
                if any(
                    self.metadata[sig].get(rank, sig) == hosts.get(rank, "NONE")
                    for hosts in self.virus_hosts[virus_species]
                )
            )
        else:
            return set(
                i
                for (i, sig) in enumerate(self.signatures)
                if self.metadata[virus].get(rank, virus)
                == self.metadata[sig].get(rank, "NONE")
            )

    @functools.lru_cache()
    def virus_relation(self, from_virus: str, to_virus: str) -> Optional[str]:
        for rank in RANKS:
            if (
                self.metadata[from_virus][rank] == self.metadata[to_virus][rank]
                and self.metadata[from_virus][rank] != ""
            ):
                return rank

        return "None"

    @functools.lru_cache()
    def host_relation(self, from_virus: str, to_host: str) -> Optional[str]:
        virus_species = self.metadata[from_virus]["species"]

        for rank in RANKS:
            for host_tax in self.virus_hosts[virus_species]:
                if self.metadata[to_host].get(rank, None) == host_tax[rank]:
                    return rank

        return "None"

    @functools.lru_cache()
    def relation(self, from_virus: str, to: str) -> Optional[str]:
        if self.metadata.get(to, None) is None:
            raise ValueError(f"Given {to} doesn't exist in metadata.")
        elif self.metadata[to]["superkingdom"] == "viruses":
            return self.virus_relation(from_virus, to)
        else:
            return self.host_relation(from_virus, to)


@functools.lru_cache(1)
def get_virus_relations():
    viruses = common.get_viruses()
    virus_metadata = common.get_virus_metadata(viruses)
    virus_hosts = common.get_virus_hosts(virus_metadata)

    return Relations(tuple(viruses), virus_metadata, virus_hosts, False)


@functools.lru_cache(1)
def with_metadata(new_metadata: Dict[str, Dict[str, Any]]):
    viruses = common.get_viruses()
    virus_metadata = common.get_virus_metadata(viruses)
    virus_hosts = common.get_virus_hosts(virus_metadata)

    return Relations(
        tuple(viruses), {**virus_metadata, **new_metadata}, virus_hosts, False
    )


def get_index_of_clade_relations(virus: str, rank: str) -> Set[int]:
    relations = get_virus_relations()
    return relations.index_of_clade_relations(virus, rank)


def virus_relation(from_virus: str, to_virus: str) -> Optional[str]:
    relations = get_virus_relations()
    return relations.virus_relation(from_virus, to_virus)


def host_relation(from_virus: str, to_host: str) -> Optional[str]:
    relations = get_virus_relations()
    return relations.host_relation(from_virus, to_host)


def relation(from_virus: str, to: str) -> Optional[str]:
    relations = get_virus_relations()
    return relations.relation(from_virus, to)
