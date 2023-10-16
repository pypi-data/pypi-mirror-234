import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.animal import (
    validate_has_animals
)


class_path = 'hestia_earth.validation.validators.animal'


def test_validate_has_animals_valid():
    # no products should be valid
    assert validate_has_animals({}) is True

    with open(f"{fixtures_path}/animal/valid.json") as f:
        cycle = json.load(f)
    assert validate_has_animals(cycle) is True


def test_validate_has_animals_invalid():
    with open(f"{fixtures_path}/animal/invalid.json") as f:
        cycle = json.load(f)
    assert validate_has_animals(cycle) == {
        'level': 'warning',
        'dataPath': '',
        'message': 'should specify the herd composition'
    }
