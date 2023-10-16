""" Module for the compound storage """
from dataclasses import dataclass
from typing import Dict, List, Tuple
from soil.storage.base_storage import BaseStorage


@dataclass
class CompoundStorage(BaseStorage):
    """
    A meta storage composed of other storages as a dict.

    Example:
        compound = CompoundStorage(storages={
            "db": Elasticsearch(index="index1"),
            "disk": ObjectStorage()
        })
        compound["second_db"] = ElasticSearch(index="index2")
        compound["db"].search(query=myquery)
    """

    storages: Dict[str, BaseStorage]

    def __getitem__(self, storage_name: str) -> BaseStorage:
        """
        Return the storage with that storage_name
        """

    def __setitem__(self, storage_name: str, storage: BaseStorage) -> None:
        """
        Set storage to that storage_name
        """

    def __len__(self) -> int:
        """
        Returns the number of storages
        """

    def items(self) -> List[Tuple[str, BaseStorage]]:
        """
        Returns an iterable of sotrage_name, storage tuples
        """
