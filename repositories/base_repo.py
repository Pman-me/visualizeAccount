from abc import ABC, abstractmethod
from typing import Optional


class BaseRepo(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, data: dict, /, key: Optional[str],):
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Deletes data from the repo
        Args:
            key (str): The key to delete data for.
        """
        pass
