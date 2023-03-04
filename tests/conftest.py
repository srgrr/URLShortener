import pytest
import os
from configparser import ConfigParser

config_file_contents = """
[server]
port=9113
logging_file=shortener.log

[backend]
implementation=files
max_generation_retries=10
url_length=6

[files]
filename=url_mappings.txt
"""


@pytest.fixture(scope="function")
def configuration():
    configparser = ConfigParser()
    configparser.read_string(config_file_contents)
    return configparser


@pytest.fixture(scope="function")
def mappings_file():
    yield "url_mappings.txt"
    if os.path.exists("url_mappings.txt"):
        os.unlink("url_mappings.txt")
    if os.path.exists("url_mappings.txt.lock"):
        os.unlink("url_mappings.txt.lock")
