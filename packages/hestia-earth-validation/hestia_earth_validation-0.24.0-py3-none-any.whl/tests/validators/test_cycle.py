from unittest.mock import patch
import os
import json
from hestia_earth.schema import SiteSiteType, CycleFunctionalUnit

from tests.utils import fixtures_path
from hestia_earth.validation.utils import _group_nodes
from hestia_earth.validation.validators.cycle import (
    validate_cycle,
    validate_cycle_aggregated,
    validate_cycle_dates,
    validate_cycleDuration,
    validate_economicValueShare,
    validate_sum_aboveGroundCropResidue,
    validate_crop_residue_complete,
    validate_crop_residue_incomplete,
    validate_siteDuration,
    validate_otherSites_cycleDuration,
    validate_possibleCoverCrop,
    validate_set_treatment,
    validate_products_animals,
    validate_single_linked_impact_assessment,
    validate_functionalUnit_not_1_ha
)

fixtures_folder = os.path.join(fixtures_path, 'cycle')
class_path = 'hestia_earth.validation.validators.cycle'
cropResidue = [
    'aboveGroundCropResidueRemoved', 'aboveGroundCropResidueIncorporated', 'aboveGroundCropResidueTotal',
    'aboveGroundCropResidueLeftOnField', 'aboveGroundCropResidueBurnt',
    'belowGroundCropResidue'
]


def test_validate_cycle_valid():
    with open(f"{fixtures_folder}/valid.json") as f:
        node = json.load(f)
    assert validate_cycle(node) == [True] * 75


def test_validate_cycle_aggregated_valid():
    with open(f"{fixtures_folder}/aggregated-valid.json") as f:
        node = json.load(f)
    assert validate_cycle_aggregated(node) == [True] * 1


def test_validate_cycle_dates_valid():
    cycle = {
        'startDate': '2020-01-01',
        'endDate': '2020-01-02'
    }
    assert validate_cycle_dates(cycle) is True
    cycle = {
        'startDate': '2020-01',
        'endDate': '2020-01'
    }
    assert validate_cycle_dates(cycle) is True
    cycle = {
        'startDate': '2020',
        'endDate': '2020'
    }
    assert validate_cycle_dates(cycle) is True


def test_validate_cycle_dates_invalid():
    cycle = {
        'startDate': '2020-01-02',
        'endDate': '2020-01-01'
    }
    assert validate_cycle_dates(cycle) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }
    cycle = {
        'startDate': '2020-01-01',
        'endDate': '2020-01-01'
    }
    assert validate_cycle_dates(cycle) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def test_validate_cycleDuration_valid():
    cycle = {
        'startDate': '2020-01-02',
        'endDate': '2021-01-01',
        'cycleDuration': 365
    }
    assert validate_cycleDuration(cycle) is True


def test_validate_cycleDuration_invalid():
    cycle = {
        'startDate': '2020-01-02',
        'endDate': '2021-01-01',
        'cycleDuration': 200
    }
    assert validate_cycleDuration(cycle) == {
        'level': 'error',
        'dataPath': '.cycleDuration',
        'message': 'must equal to endDate - startDate in days (~365.0)'
    }


def test_validate_economicValueShare_valid():
    products = [{
        'economicValueShare': 10
    }, {
        'economicValueShare': 80
    }]
    assert validate_economicValueShare(products) is True


def test_validate_economicValueShare_invalid():
    products = [{
        'economicValueShare': 10
    }, {
        'economicValueShare': 90
    }, {
        'economicValueShare': 10
    }]
    assert validate_economicValueShare(products) == {
        'level': 'error',
        'dataPath': '.products',
        'message': 'economicValueShare should sum to 100 or less across all products',
        'params': {
            'sum': 110
        }
    }


def test_validate_sum_aboveGroundCropResidue_valid():
    with open(f"{fixtures_folder}/aboveGroundCropResidue/valid.json") as f:
        data = json.load(f)
    assert validate_sum_aboveGroundCropResidue(data.get('products')) is True


def test_validate_sum_aboveGroundCropResidue_invalid():
    with open(f"{fixtures_folder}/aboveGroundCropResidue/invalid.json") as f:
        data = json.load(f)
    assert validate_sum_aboveGroundCropResidue(data.get('products')) == {
        'level': 'error',
        'dataPath': '.products[0].value',
        'message': 'must be more than or equal to '
        '(aboveGroundCropResidueBurnt + aboveGroundCropResidueLeftOnField)'
    }


@patch(f"{class_path}.get_crop_residue_terms", return_value=cropResidue)
def test_validate_crop_residue_complete_valid(*args):
    with open(f"{fixtures_folder}/cropResidue/complete/valid.json") as f:
        data = json.load(f)
    assert validate_crop_residue_complete(data, data.get('site')) is True


@patch(f"{class_path}.get_crop_residue_terms", return_value=cropResidue)
def test_validate_crop_residue_complete_invalid(*args):
    with open(f"{fixtures_folder}/cropResidue/complete/invalid.json") as f:
        data = json.load(f)
    assert validate_crop_residue_complete(data, data.get('site')) == {
        'level': 'error',
        'dataPath': '',
        'message': 'must specify the fate of cropResidue',
        'params': {
            'siteType': ['cropland', 'glass or high accessible cover']
        }
    }


def test_validate_crop_residue_incomplete_valid():
    with open(f"{fixtures_folder}/cropResidue/incomplete/valid.json") as f:
        data = json.load(f)
    assert validate_crop_residue_incomplete(data, data.get('site')) is True


def test_validate_crop_residue_incomplete_invalid():
    with open(f"{fixtures_folder}/cropResidue/incomplete/invalid.json") as f:
        data = json.load(f)
    assert validate_crop_residue_incomplete(data, data.get('site')) == {
        'level': 'warning',
        'dataPath': '',
        'message': 'should specify the fate of cropResidue',
        'params': {
            'siteType': ['cropland', 'glass or high accessible cover']
        }
    }


def test_validate_siteDuration_valid():
    with open(f"{fixtures_folder}/siteDuration/valid.json") as f:
        data = json.load(f)
    assert validate_siteDuration(data) is True

    with open(f"{fixtures_folder}/siteDuration/valid-no-siteDuration.json") as f:
        data = json.load(f)
    assert validate_siteDuration(data) is True

    with open(f"{fixtures_folder}/siteDuration/valid-otherSites.json") as f:
        data = json.load(f)
    assert validate_siteDuration(data) is True


def test_validate_siteDuration_invalid():
    with open(f"{fixtures_folder}/siteDuration/invalid.json") as f:
        data = json.load(f)
    assert validate_siteDuration(data) == {
        'level': 'error',
        'dataPath': '.siteDuration',
        'message': 'must be equal to cycleDuration'
    }

    with open(f"{fixtures_folder}/siteDuration/invalid-otherSites.json") as f:
        data = json.load(f)
    assert validate_siteDuration(data) == {
        'level': 'error',
        'dataPath': '.siteDuration',
        'message': 'must not be equal to cycleDuration'
    }


def test_validate_otherSites_cycleDuration_valid():
    with open(f"{fixtures_folder}/otherSites/cycleDuration/valid.json") as f:
        data = json.load(f)
    assert validate_otherSites_cycleDuration(data) is True

    with open(f"{fixtures_folder}/otherSites/cycleDuration/valid-no-siteDuration.json") as f:
        data = json.load(f)
    assert validate_siteDuration(data) is True


def test_validate_otherSites_cycleDuration_invalid():
    with open(f"{fixtures_folder}/otherSites/cycleDuration/invalid.json") as f:
        data = json.load(f)
    assert validate_otherSites_cycleDuration(data) == {
        'level': 'error',
        'dataPath': '.cycleDuration',
        'message': 'must be equal to the sum of siteDuration and otherSitesDuration'
    }


def test_validate_possibleCoverCrop_valid():
    # no products should be valid
    assert validate_possibleCoverCrop({}) is True

    with open(f"{fixtures_folder}/coverCrop/valid.json") as f:
        data = json.load(f)
    assert validate_possibleCoverCrop(data) is True

    with open(f"{fixtures_folder}/coverCrop/valid-not-coverCrop.json") as f:
        data = json.load(f)
    assert validate_possibleCoverCrop(data) is True


def test_validate_possibleCoverCrop_error():
    with open(f"{fixtures_folder}/coverCrop/invalid.json") as f:
        data = json.load(f)
    assert validate_possibleCoverCrop(data) == {
        'level': 'error',
        'dataPath': '',
        'message': 'cover crop cycle contains non cover crop product'
    }


def test_validate_set_treatment_valid():
    cycle = {'treatment': 'treatment'}

    # no experimentDesign in Source
    source = {}
    validate_set_treatment(cycle, source) is True

    # with experimentDesign and treatment
    source = {'experimentDesign': 'design'}
    validate_set_treatment(cycle, source) is True


def test_validate_set_treatment_warning():
    source = {'experimentDesign': 'design'}
    cycle = {}
    assert validate_set_treatment(cycle, source) == {
        'level': 'warning',
        'dataPath': '.treatment',
        'message': 'should specify a treatment when experimentDesign is specified'
    }


def test_validate_products_animals_valid():
    # no products should be valid
    assert validate_products_animals({}) is True

    with open(f"{fixtures_folder}/products/animals/valid.json") as f:
        data = json.load(f)
    assert validate_products_animals(data) is True


def test_validate_products_animals_invalid():
    with open(f"{fixtures_folder}/products/animals/invalid.json") as f:
        data = json.load(f)
    assert validate_products_animals(data) == {
        'level': 'warning',
        'dataPath': '.products',
        'message': 'should not specify both liveAnimal and animalProduct'
    }


def test_validate_single_linked_impact_assessment_valid():
    with open(f"{fixtures_folder}/product-single-ia/cycle.json") as f:
        cycle = json.load(f)
    with open(f"{fixtures_folder}/product-single-ia/valid.json") as f:
        nodes = json.load(f).get('nodes')
    assert validate_single_linked_impact_assessment(cycle, _group_nodes(nodes)) is True


def test_validate_single_linked_impact_assessment_invalid():
    with open(f"{fixtures_folder}/product-single-ia/cycle.json") as f:
        cycle = json.load(f)
    with open(f"{fixtures_folder}/product-single-ia/invalid.json") as f:
        nodes = json.load(f).get('nodes')
    assert validate_single_linked_impact_assessment(cycle, _group_nodes(nodes)) == {
        'level': 'error',
        'dataPath': '.products[0].term',
        'message': 'multiple ImpactAssessment are associated with this Product',
        'params': {
            'product': {
                '@type': 'Product',
                'term': {
                    '@type': 'Term',
                    '@id': 'maizeGrain'
                },
                'fate': 'sold'
            },
            'node': {
                'type': 'Cycle',
                'id': 'fake-cycle'
            }
        }
    }


def test_validate_functionalUnit_not_1_ha_valid():
    cycle = {
        'functionalUnit': CycleFunctionalUnit.RELATIVE.value
    }
    site = {
        'siteType': SiteSiteType.AGRI_FOOD_PROCESSOR.value
    }
    assert validate_functionalUnit_not_1_ha(cycle, site) is True


def test_validate_functionalUnit_not_1_ha_invalid():
    cycle = {
        'functionalUnit': CycleFunctionalUnit._1_HA.value
    }
    site = {
        'siteType': SiteSiteType.AGRI_FOOD_PROCESSOR.value
    }
    assert validate_functionalUnit_not_1_ha(cycle, site) == {
        'level': 'error',
        'dataPath': '.functionalUnit',
        'message': 'must not be equal to 1 ha',
        'params': {
            'siteType': site.get('siteType')
        }
    }
