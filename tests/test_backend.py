from server.backend import get_backend, FileSystemBackend


def test_backend_factory_files_class(configuration, mappings_file):
    configuration["backend"]["implementation"] = "files"
    backend = get_backend(configuration)
    assert isinstance(backend, FileSystemBackend),\
        f"Backend should be of type FileSystemBackend, got {backend.__class__} instead"
    assert configuration["files"]["filename"] == backend.filename
    assert configuration["backend"]["max_generation_retries"] == backend.max_generation_retries
    assert configuration["backend"]["url_length"] == backend.url_length


def test_backend_filesystem_write_url(configuration, mappings_file):
    configuration["backend"]["implementation"] = "files"
    backend = get_backend(configuration)
    backend.insert_new_url("long_url_1", "short_url_1")
    backend.insert_new_url("long_url_2", "short_url_2")
    # Read is out of scope, do it manually!
    with open(mappings_file, "r") as f:
        entries = {k: v for (k, v) in map(lambda x: map(str.strip, x.strip().split("->")), f.readlines())}

    assert entries == {"short_url_1": "long_url_1", "short_url_2": "long_url_2"},\
        f"Filesystem entries are {entries}"
