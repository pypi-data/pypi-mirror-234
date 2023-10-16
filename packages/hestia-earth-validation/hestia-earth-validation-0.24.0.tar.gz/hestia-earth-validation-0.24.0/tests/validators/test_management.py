import os
import json
from hestia_earth.schema import TermTermType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.management import (
    validate_has_termType,
    validate_has_termTypes,
    validate_exists
)

fixtures_folder = os.path.join(fixtures_path, 'management')


def test_validate_has_termType_valid():
    with open(f"{fixtures_folder}/termType/valid-cropland.json") as f:
        site = json.load(f)

    assert validate_has_termType(site, TermTermType.LANDUSEMANAGEMENT) is True

    with open(f"{fixtures_folder}/termType/valid-permanent-pasture.json") as f:
        site = json.load(f)

    assert validate_has_termType(site, TermTermType.LANDUSEMANAGEMENT) is True


def test_validate_has_termType_invalid():
    with open(f"{fixtures_folder}/termType/invalid-cropland.json") as f:
        site = json.load(f)

    assert validate_has_termType(site, TermTermType.LANDUSEMANAGEMENT) == {
        'level': 'warning',
        'dataPath': '.management',
        'message': 'should contain at least one management node',
        'params': {
            'termType': 'landUseManagement'
        }
    }

    with open(f"{fixtures_folder}/termType/invalid-permanent-pasture.json") as f:
        site = json.load(f)

    assert validate_has_termType(site, TermTermType.WATERREGIME) == {
        'level': 'warning',
        'dataPath': '.management',
        'message': 'should contain at least one management node',
        'params': {
            'termType': 'waterRegime'
        }
    }


def test_validate_has_termTypes_valid():
    # no blank node is valid
    site = {}
    assert validate_has_termTypes(site) is True

    with open(f"{fixtures_folder}/termType/valid-cropland.json") as f:
        site = json.load(f)

    assert validate_has_termTypes(site) is True

    with open(f"{fixtures_folder}/termType/valid-permanent-pasture.json") as f:
        site = json.load(f)

    assert validate_has_termTypes(site) is True

    with open(f"{fixtures_folder}/termType/valid-no-management.json") as f:
        site = json.load(f)

    assert validate_has_termTypes(site) is True


def test_validate_has_termTypes_invalid():
    with open(f"{fixtures_folder}/termType/invalid-cropland.json") as f:
        site = json.load(f)

    assert validate_has_termTypes(site) == [
        {
            'level': 'warning',
            'dataPath': '.management',
            'message': 'should contain at least one management node',
            'params': {
                'termType': 'landUseManagement'
            }
        },
        {
            'level': 'warning',
            'dataPath': '.management',
            'message': 'should contain at least one management node',
            'params': {
                'termType': 'waterRegime'
            }
        }
    ]

    with open(f"{fixtures_folder}/termType/invalid-permanent-pasture.json") as f:
        site = json.load(f)

    assert validate_has_termTypes(site) == [
        {
            'level': 'warning',
            'dataPath': '.management',
            'message': 'should contain at least one management node',
            'params': {
                'termType': 'landUseManagement'
            }
        },
        {
            'level': 'warning',
            'dataPath': '.management',
            'message': 'should contain at least one management node',
            'params': {
                'termType': 'waterRegime'
            }
        }
    ]


def test_validate_exists_valid():
    with open(f"{fixtures_folder}/exists/valid.json") as f:
        site = json.load(f)

    assert validate_exists(site) is True


def test_validate_exists_invalid():
    with open(f"{fixtures_folder}/exists/invalid.json") as f:
        site = json.load(f)

    assert validate_exists(site) == {
        'level': 'warning',
        'dataPath': '.management',
        'message': 'should contain at least one management node'
    }
