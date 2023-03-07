from .file_system_backend import FileSystemBackend
from .redis_backend import RedisBackend
from configparser import ConfigParser


def get_backend(configuration: ConfigParser):
    implementation = configuration["backend"]["implementation"]

    backend_config = configuration["backend"]
    # args common to all backends
    args = {
        "max_generation_retries": backend_config["max_generation_retries"],
        "url_length": backend_config["url_length"],
        "url_pool": backend_config["url_pool"]
    }

    if implementation == "files":
        args.update(
            {
                "filename": configuration["files"]["filename"]
            }
        )
        return FileSystemBackend(**args)
    if implementation == "redis":
        redis_config = configuration["redis"]
        args.update(
            {
                "host": redis_config["host"],
                "port": redis_config["port"],
                "username": redis_config["username"],
                "password": redis_config["password"],
                "bucket_size": redis_config["bucket_size"]
            }
        )
        return RedisBackend(**args)
    raise TypeError(f"Specified implementation {implementation} doesn't exist, check configuration.ini")
