import os
from .backend import Backend
from string import ascii_lowercase, digits
from random import choice
from filelock import FileLock


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
        if not os.path.exists(self.filename):
            with self._get_lock():
                with open(self.filename, "a"):
                    pass
        super().__init__(**kwargs)
