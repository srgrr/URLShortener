from file_system_backend import FileSystemBackend


def get_backend(configuration):
    implementation = configuration["backend"]["implementation"]
    if implementation == "files":
        return FileSystemBackend(
            filename=configuration["files"]["filename"],
            max_generation_retries=int(configuration["backend"]["max_generation_retries"]),
            url_length=int(configuration["backend"]["url_length"])
        )
    raise TypeError(f"Specified implementation {implementation} doesn't exist, check configuration.ini")