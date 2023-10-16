from unittest.mock import patch
import json

from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.practice import (
    validate_defaultValue,
    validate_cropResidueManagement,
    validate_waterRegime,
    validate_waterRegime_rice_products,
    validate_longFallowPeriod,
    validate_excretaManagement,
    validate_no_tillage,
    validate_tillage_site_type,
    validate_tillage_values,
    validate_liveAnimal_system,
    validate_pastureGrass_key_units,
    validate_pastureGrass_key_value,
    validate_has_pastureGrass
)

class_path = 'hestia_earth.validation.validators.practice'
RICE_TERM_IDS = ['riceMeal', 'riceGrainInHuskUpland']


def test_validate_defaultValue_valid():
    # no practices should be valid
    assert validate_defaultValue({}) is True

    with open(f"{fixtures_path}/practice/defaultValue/valid.json") as f:
        data = json.load(f)
    assert validate_defaultValue(data, 'nodes') is True


def test_validate_defaultValue_invalid():
    with open(f"{fixtures_path}/practice/defaultValue/invalid.json") as f:
        data = json.load(f)
    assert validate_defaultValue(data, 'nodes') == {
        'level': 'warning',
        'dataPath': '.nodes[0]',
        'message': 'should specify a value when Hestia has a default one',
        'params': {
            'term': {
                '@type': 'Term',
                '@id': 'irrigated',
                'termType': 'waterRegime'
            },
            'expected': 100
        }
    }


def test_validate_cropResidueManagement_valid():
    # no practices should be valid
    assert validate_cropResidueManagement([]) is True

    with open(f"{fixtures_path}/practice/cropResidueManagement/valid.json") as f:
        data = json.load(f)
    assert validate_cropResidueManagement(data.get('nodes')) is True


def test_validate_cropResidueManagement_invalid():
    with open(f"{fixtures_path}/practice/cropResidueManagement/invalid.json") as f:
        data = json.load(f)
    assert validate_cropResidueManagement(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across crop residue management practices',
        'params': {
            'sum': 110
        }
    }


def test_validate_waterRegime_valid():
    # no practices should be valid
    assert validate_waterRegime([]) is True

    with open(f"{fixtures_path}/practice/waterRegime/valid.json") as f:
        data = json.load(f)
    assert validate_waterRegime(data.get('nodes')) is True


def test_validate_waterRegime_invalid():
    with open(f"{fixtures_path}/practice/waterRegime/invalid.json") as f:
        data = json.load(f)
    assert validate_waterRegime(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across water regime practices',
        'params': {
            'sum': 110
        }
    }


@patch(f"{class_path}.get_rice_terms", return_value=RICE_TERM_IDS)
def test_validate_waterRegime_rice_products_valid(*args):
    # no practices should be valid
    assert validate_waterRegime_rice_products({}, 'practices') is True

    with open(f"{fixtures_path}/practice/waterRegime/rice/valid.json") as f:
        cycle = json.load(f)
    assert validate_waterRegime_rice_products(cycle) is True


@patch(f"{class_path}.get_rice_terms", return_value=RICE_TERM_IDS)
def test_validate_waterRegime_rice_products_invalid(*args):
    with open(f"{fixtures_path}/practice/waterRegime/rice/invalid.json") as f:
        cycle = json.load(f)
    assert validate_waterRegime_rice_products(cycle) == {
        'level': 'error',
        'dataPath': '.practices[0].term',
        'message': 'rice products not allowed for this water regime practice',
        'params': {
            'term': {
                '@type': 'Term',
                '@id': 'numberOfIrrigations',
                'termType': 'waterRegime'
            },
            'products': [{
                '@type': 'Term',
                '@id': 'riceMeal',
                'termType': 'crop'
            }]
        }
    }


def test_validate_longFallowPeriod_valid():
    # no practices should be valid
    assert validate_longFallowPeriod([]) is True

    with open(f"{fixtures_path}/practice/longFallowPeriod/valid.json") as f:
        data = json.load(f)
    assert validate_longFallowPeriod(data.get('nodes')) is True


def test_validate_longFallowPeriod_invalid():
    with open(f"{fixtures_path}/practice/longFallowPeriod/invalid.json") as f:
        data = json.load(f)
    assert validate_longFallowPeriod(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices[1].value',
        'message': 'longFallowPeriod must be lower than 5 years'
    }


def test_validate_excretaManagement_valid():
    # no practices should be valid
    assert validate_excretaManagement({}, []) is True

    with open(f"{fixtures_path}/practice/excretaManagement/valid.json") as f:
        cycle = json.load(f)
    assert validate_excretaManagement(cycle, cycle.get('practices')) is True


def test_validate_excretaManagement_invalid():
    with open(f"{fixtures_path}/practice/excretaManagement/invalid.json") as f:
        cycle = json.load(f)
    assert validate_excretaManagement(cycle, cycle.get('practices')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'an excreta input is required when using an excretaManagement practice'
    }


def test_validate_no_tillage_valid():
    # no practices should be valid
    assert validate_no_tillage([]) is True

    with open(f"{fixtures_path}/practice/noTillage/valid.json") as f:
        data = json.load(f)
    assert validate_no_tillage(data.get('nodes')) is True

    # value is not 100
    with open(f"{fixtures_path}/practice/noTillage/valid-value-not-100.json") as f:
        data = json.load(f)
    assert validate_no_tillage(data.get('nodes')) is True


def test_validate_no_tillage_invalid():
    with open(f"{fixtures_path}/practice/noTillage/invalid.json") as f:
        data = json.load(f)
    assert validate_no_tillage(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices[1]',
        'message': 'is not allowed in combination with noTillage'
    }


def test_validate_tillage_site_type_valid():
    # no practices should be valid
    assert validate_tillage_site_type([], {}) is True

    with open(f"{fixtures_path}/practice/tillage-siteType/valid.json") as f:
        cycle = json.load(f)
    assert validate_tillage_site_type(cycle.get('practices'), cycle.get('site')) is True

    # no practice but skipped termType
    with open(f"{fixtures_path}/practice/tillage-siteType/warning.json") as f:
        cycle = json.load(f)
    site = cycle.get('site')
    site['siteType'] = SiteSiteType.SEA_OR_OCEAN.value
    assert validate_tillage_site_type(cycle.get('practices'), site) is True


def test_validate_tillage_site_type_warning():
    with open(f"{fixtures_path}/practice/tillage-siteType/warning.json") as f:
        cycle = json.load(f)
    assert validate_tillage_site_type(cycle.get('practices'), cycle.get('site')) == {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should contain a tillage practice'
    }


def test_validate_tillage_values_valid():
    # no practices should be valid
    assert validate_tillage_values([]) is True

    with open(f"{fixtures_path}/practice/tillage-values/valid-no-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) is True

    with open(f"{fixtures_path}/practice/tillage-values/valid-with-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) is True


def test_validate_tillage_values_invalid():
    with open(f"{fixtures_path}/practice/tillage-values/invalid-all-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'sum not equal to 100% for tillage practices',
        'params': {
            'sum': 90
        }
    }

    with open(f"{fixtures_path}/practice/tillage-values/invalid-mixed-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'must set value for every tillage practice'
    }

    with open(f"{fixtures_path}/practice/tillage-values/invalid-no-values.json") as f:
        data = json.load(f)
    assert validate_tillage_values(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'can only have 1 tillage practice without a value',
        'params': {
            'current': [
                {
                    "@id": "stripTillage",
                    "@type": "Term",
                    "termType": "tillage"
                },
                {
                    "@id": "mulchTillage",
                    "@type": "Term",
                    "termType": "tillage"
                }
            ]
        }
    }


def test_validate_liveAnimal_system_valid():
    # no practices should be valid
    assert validate_liveAnimal_system({}) is True

    with open(f"{fixtures_path}/practice/liveAnimal-system/valid.json") as f:
        data = json.load(f)
    assert validate_liveAnimal_system(data) is True


def test_validate_liveAnimal_system_invalid():
    with open(f"{fixtures_path}/practice/liveAnimal-system/invalid.json") as f:
        data = json.load(f)
    assert validate_liveAnimal_system(data) == {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should add an animal production system'
    }


def test_validate_pastureGrass_key_units_valid():
    # no practices should be valid
    assert validate_pastureGrass_key_units({}) is True

    with open(f"{fixtures_path}/practice/pastureGrass/key-units/valid.json") as f:
        practice = json.load(f)
    assert validate_pastureGrass_key_units({'practices': [practice]}) is True


def test_validate_pastureGrass_key_units_invalid():
    with open(f"{fixtures_path}/practice/pastureGrass/key-units/invalid.json") as f:
        practice = json.load(f)
    assert validate_pastureGrass_key_units({'practices': [practice]}) == {
        'level': 'error',
        'dataPath': '.practices[0].key',
        'message': "pastureGrass key units must be 'ha'",
        'params': {
            'expected': 'ha',
            'term': {'@id': 'alfalfaFreshForage', '@type': 'Term', 'units': 'kg'},
            'value': 'kg'
        }
    }


def test_validate_pastureGrass_key_value_valid():
    # no practices should be valid
    assert validate_pastureGrass_key_value({}) is True

    with open(f"{fixtures_path}/practice/pastureGrass/key-value/valid.json") as f:
        cycle = json.load(f)
    assert validate_pastureGrass_key_value(cycle, 'practices') is True


def test_validate_pastureGrass_key_value_invalid():
    with open(f"{fixtures_path}/practice/pastureGrass/key-value/invalid.json") as f:
        cycle = json.load(f)
    assert validate_pastureGrass_key_value(cycle, 'practices') == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'the sum of all pastureGrass values must be 100',
        'params': {
            'expected': 100,
            'current': 80
        }
    }

    with open(f"{fixtures_path}/practice/pastureGrass/key-value/invalid-numbers.json") as f:
        cycle = json.load(f)
    assert validate_pastureGrass_key_value(cycle, 'practices') == {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'all values must be numbers'
    }


def test_validate_has_pastureGrass_valid():
    with open(f"{fixtures_path}/practice/pastureGrass/permanent-pasture/valid.json") as f:
        data = json.load(f)
    assert validate_has_pastureGrass(data, data.get('site'), 'practices') is True


def test_validate_has_pastureGrass_invalid():
    with open(f"{fixtures_path}/practice/pastureGrass/permanent-pasture/invalid.json") as f:
        data = json.load(f)
    assert validate_has_pastureGrass(data, data.get('site')) == {
        'level': 'warning',
        'dataPath': '.practices',
        'message': 'should add the term pastureGrass'
    }
