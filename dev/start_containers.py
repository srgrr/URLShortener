import argparse
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(
        'Setup a local environment for testing purposes'
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
        '--stop-rm-only',
        action='store_true',
        help='Only stop and delete already existing containers'
    )
    return parser.parse_args()


def main(redis_port, redis_insight_port, stop_rm_only, schema_only):
    if not schema_only:
        stop_rm_only_val = 'true' if stop_rm_only else 'false'
        subprocess.call(
            [
                './run_db_containers.sh',
                f'{redis_port}',
                f'{redis_insight_port}',
                stop_rm_only_val
            ]
        )


if __name__ == '__main__':
    opts = parse_args()
    main(**vars(opts))
else:
    raise ImportError('This is not a Python Module and it should never be imported!')