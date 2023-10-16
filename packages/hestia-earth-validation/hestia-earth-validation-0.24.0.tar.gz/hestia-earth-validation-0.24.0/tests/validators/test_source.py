import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.source import validate_source

class_path = 'hestia_earth.validation.validators.source'


def test_validate_valid():
    with open(f"{fixtures_path}/source/valid.json") as f:
        node = json.load(f)
    assert validate_source(node) == [True] * 1
