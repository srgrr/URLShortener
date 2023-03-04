import pytest
import os
from configparser import ConfigParser

config_file_contents = """
[server]
port=8080
logging_file=shortener.log

[backend]
implementation=files
max_generation_retries=10
url_length=6

[files]
filename=url_mappings.txt
"""
test_file_name = "url_mappings.txt"


@pytest.fixture(scope="function")
def configuration():
    configparser = ConfigParser()
    configparser.read_string(config_file_contents)
    return configparser


@pytest.fixture(scope="function")
def mappings_file():
    yield test_file_name
    if os.path.exists(test_file_name):
        os.unlink(test_file_name)
    if os.path.exists(f"{test_file_name}.lock"):
        os.unlink(f"{test_file_name}.lock")
