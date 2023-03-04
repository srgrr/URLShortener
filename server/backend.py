import os
from abc import ABC, abstractmethod
from typing import Optional
from filelock import FileLock
from random import choice
from string import ascii_lowercase, digits


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


class FileSystemBackend(Backend):

    def _get_random_string(self, pool=ascii_lowercase + digits):
        return ''.join(choice(pool) for _ in range(self.url_length))

    def _get_lock(self):
        return FileLock(f"{self.filename}.lock")

    def get_new_url(self) -> str:
        for _ in range(self.max_generation_retries):
            with self._get_lock():
                candidate = self._get_random_string()
                for line in open(self.filename, "r"):
                    short, _ = map(str.strip, line.strip().split("->"))
                    if short == candidate:
                        break
                else:
                    return candidate
        raise KeyError(f"Couldn't get short URL")

    def insert_new_url(self, long_url: str, short_url: str) -> None:
        with self._get_lock():
            with open(self.filename, "a") as f:
                f.write(f"{short_url} -> {long_url}\n")

    def get_long_url(self, short_url: str):
        for line in open(self.filename, "r"):
            short, long = map(str.strip, line.strip().split("->"))
            if short == short_url:
                return long
        return None

    def __init__(self, **kwargs):
        self.filename = kwargs.pop("filename")
        self.max_generation_retries = kwargs.pop("max_generation_retries")
        self.url_length = kwargs.pop("url_length")
        if not os.path.exists(self.filename):
            with self._get_lock():
                with open(self.filename, "a") as f:
                    pass
        super().__init__(**kwargs)


def get_backend(configuration):
    implementation = configuration["backend"]["implementation"]
    if implementation == "files":
        return FileSystemBackend(
            filename=configuration["files"]["filename"],
            max_generation_retries=int(configuration["backend"]["max_generation_retries"]),
            url_length=int(configuration["backend"]["url_length"])
        )
    raise TypeError(f"Specified implementation {implementation} doesn't exist, check configuration.ini")