import os
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.impact_assessment import (
    validate_impact_assessment,
    validate_impact_assessment_aggregated,
    validate_linked_cycle_product,
    validate_linked_cycle_endDate
)

fixtures_folder = os.path.join(fixtures_path, 'impactAssessment')


def test_validate_impact_assessment_valid():
    with open(f"{fixtures_folder}/valid.json") as f:
        node = json.load(f)
    assert validate_impact_assessment(node) == [True] * 19


def test_validate_impact_assessment_aggregated_valid():
    with open(f"{fixtures_folder}/aggregated-valid.json") as f:
        node = json.load(f)
    assert validate_impact_assessment_aggregated(node) == [True] * 1


def test_validate_linked_cycle_product_valid():
    with open(f"{fixtures_folder}/cycle-contains-product/valid.json") as f:
        data = json.load(f)
    assert validate_linked_cycle_product(data, data.get('cycle')) is True


def test_validate_linked_cycle_product_invalid():
    with open(f"{fixtures_folder}/cycle-contains-product/invalid.json") as f:
        data = json.load(f)
    assert validate_linked_cycle_product(data, data.get('cycle')) == {
        'level': 'error',
        'dataPath': '.product',
        'message': 'should be included in the cycle products',
        'params': {
            'product': {
                '@type': 'Term',
                '@id': 'maizeGrain'
            },
            'node': {
                'type': 'Cycle',
                'id': 'fake-cycle'
            }
        }
    }


def test_validate_linked_cycle_endDate_valid():
    with open(f"{fixtures_folder}/cycle-endDate/valid.json") as f:
        data = json.load(f)
    assert validate_linked_cycle_endDate(data, data.get('cycle')) is True


def test_validate_linked_cycle_endDate_invalid():
    with open(f"{fixtures_folder}/cycle-endDate/invalid.json") as f:
        data = json.load(f)
    assert validate_linked_cycle_endDate(data, data.get('cycle')) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be equal to the Cycle endDate'
    }
