import argparse
import logging
import subprocess
import redis


def parse_args():
    parser = argparse.ArgumentParser(
        'Setup a local environment for testing purposes'
    )
    parser.add_argument(
        '--redis-host',
        type=str,
        default='localhost',
        help='Redis Host'
    )
    parser.add_argument(
        '--redis-port',
        type=int,
        default=6379,
        help='Redis Port'
    )
    parser.add_argument(
        '--redis-insight-port',
        type=int,
        default=8001,
        help='Redis Insight Port'
    )
    parser.add_argument(
        '--redis-bucket-size',
        type=int,
        default=16384,
        help='Hash bucket size'
    )
    parser.add_argument(
        '--url-length',
        type=int,
        default=6,
        help='URL length'
    )
    parser.add_argument(
        '--url-alphabet-size',
        type=int,
        default=26 * 2 + 10,
        help='URL alphabet size'
    )
    parser.add_argument(
        '--stop-rm-only',
        action='store_true',
        help='Only stop and delete already existing containers'
    )
    return parser.parse_args()


def _configure_logger():
    args = {
        "level": logging.DEBUG,
        "format": "%(asctime)s %(levelname)-8s %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S"
    }
    logging.basicConfig(**args)


def main(redis_host, redis_port, redis_insight_port, redis_bucket_size, url_length, url_alphabet_size, stop_rm_only):
    _configure_logger()
    stop_rm_only_val = 'true' if stop_rm_only else 'false'
    subprocess.call(
        [
            './db_containers.sh',
            f'{redis_port}',
            f'{redis_insight_port}',
            stop_rm_only_val
        ]
    )
    if not stop_rm_only:
        total_urls = url_alphabet_size ** url_length
        logging.debug(f"Total URLS: {total_urls}")
        num_buckets = (total_urls + redis_bucket_size - 1) // redis_bucket_size
        logging.debug(f"Num buckets: {num_buckets}")
        redis_client = redis.Redis(
            connection_pool=redis.ConnectionPool(
                host=redis_host,
                port=redis_port
            )
        )
        for start in range(0, num_buckets, 20000):
            bucket_ids = list(range(start, start + 20000))
            redis_client.sadd("free_buckets", *bucket_ids)


if __name__ == '__main__':
    opts = parse_args()
    main(**vars(opts))
else:
    raise ImportError('This is not a Python Module and it should never be imported!')