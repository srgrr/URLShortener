import pytest
from server.backend_accessor import get_backend
from server.redis_backend import RedisBackend


def test_backend_factory_redis_class(configuration):
    configuration["backend"]["implementation"] = "redis"
    backend = get_backend(configuration)
    assert isinstance(backend, RedisBackend),\
        f"Backend should be of type FileSystemBackend, got {backend.__class__} instead"
    assert int(configuration["backend"]["max_generation_retries"]) == backend.max_generation_retries
    assert int(configuration["backend"]["url_length"]) == backend.url_length


@pytest.mark.parametrize(
    "short_url, expected_encoding",
    [
        ("aaa", 0),
        ("9aa", 61),
        ("aba", 62)
    ]
)
def test_redis_backend_short2number(configuration, short_url, expected_encoding):
    configuration["backend"]["implementation"] = "redis"
    backend: RedisBackend = get_backend(configuration)
    received_encoding = backend._short2number(short_url)
    assert received_encoding == expected_encoding,\
        f"Encoded {short_url} as {received_encoding} (expected: {expected_encoding})"


@pytest.mark.parametrize(
    "expected_short, encoding",
    [
        ("aaa", 0),
        ("9aa", 61),
        ("aba", 62)
    ]
)
def test_redis_backend_short2number(configuration, expected_short, encoding):
    configuration["backend"]["implementation"] = "redis"
    backend: RedisBackend = get_backend(configuration)
    received_short = backend._number2short(encoding)
    assert received_short == expected_short,\
    f"Decoded {encoding} as {received_short} (expected: {expected_short})"

