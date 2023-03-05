from abc import ABC, abstractmethod
from typing import Optional


class Backend(ABC):
    @abstractmethod
    def get_new_url(self) -> str:
        """Get a new shortened URL. It must be unique and not exist in the URL DB
        :return: str consisting of lowercase letters and digits [a-z0-9]
        """
        pass

    @abstractmethod
    def insert_new_url(self, long_url: str, short_url: str) -> None:
        """Insert a mapping short -> long into the DB
        :param long_url: str
        :param short_url: str
        :return: None
        """
        pass

    @abstractmethod
    def get_long_url(self, short_url: str) -> Optional[str]:
        """Get the mapping short -> long for a shortened URL (or None if it doesn't exist)
        :param short_url: str
        :return: str or None
        """
        pass

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
