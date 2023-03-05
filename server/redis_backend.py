import redis
from typing import Optional
from backend import Backend
from random import choice


class RedisBackend(Backend):
    def get_new_url(self) -> str:
        bucket = int(self.r.srandmember("free_buckets"))
        bucket_key = f"bucket_{bucket}"

        keys_in_bucket = self.r.get(bucket_key) or set()
        lowest_key, highest_key = bucket * self.bucket_size, bucket * (self.bucket_size + 1)
        potential_keys = set(list(range(lowest_key, highest_key)))

        chosen_key = choice(list(potential_keys - keys_in_bucket))
        self.r.sadd(bucket_key, chosen_key)
        if self.r.scard(bucket_key) == self.bucket_size:
            self.r.srem("free_buckets", bucket_key)

        return self._number2short(int(chosen_key))

    def insert_new_url(self, long_url: str, short_url: str) -> None:
        self.r.set(f"URL_{self._short2number(short_url)}", long_url)

    def get_long_url(self, short_url: str) -> Optional[str]:
        fetched_url = self.r.get(f"URL_{self._short2number(short_url)}")
        if fetched_url:
            return fetched_url.decode("utf-8")

    def _get_redis_client(self):
        return redis.Redis(
            connection_pool=redis.ConnectionPool(
                host=self.host,
                port=self.port
            ),
            username=self.username,
            password=self.password
        )

    def _short2number(self, short: str) -> int:
        return sum(
            (len(self.url_pool) ** i) * self.val2pos[x]
            for (i, x) in enumerate(short)
        )

    def _number2short(self, number: int) -> str:
        ret = ''
        for _ in range(self.url_length):
            ret += self.url_pool[number % len(self.url_pool)]
            number = number // len(self.url_pool)
        return ret

    def __init__(self, **kwargs):
        self.host = kwargs.pop("host")
        self.port = int(kwargs.pop("port"))
        self.username = kwargs.pop("username")
        self.password = kwargs.pop("password")
        self.bucket_size = int(kwargs.pop("bucket_size"))
        super().__init__(**kwargs)

        self.r = self._get_redis_client()
        self.val2pos = {
            k: v for (v, k) in enumerate(self.url_pool)
        }
