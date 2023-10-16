from hestia_earth.schema import SiteSiteType, TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import list_sum

from hestia_earth.validation.utils import _filter_list_errors, is_live_animal_cycle
from hestia_earth.validation.terms import get_fuel_terms, get_forage_terms


def _validate_cropland(data_completeness: dict, site: dict):
    validate_keys = [
        'animalFeed',
        TermTermType.EXCRETA.value
    ]
    site_type = site.get('siteType')

    def validate_key(key: str):
        return data_completeness.get(key) is True or {
            'level': 'warning',
            'dataPath': f".completeness.{key}",
            'message': f"should be true for site of type {site_type}"
        }

    return site_type not in [
        SiteSiteType.CROPLAND.value,
        SiteSiteType.GLASS_OR_HIGH_ACCESSIBLE_COVER.value
    ] or _filter_list_errors(map(validate_key, validate_keys))


def _validate_all_values(data_completeness: dict):
    values = data_completeness.values()
    return next((value for value in values if isinstance(value, bool) and value is True), False) or {
        'level': 'warning',
        'dataPath': '.completeness',
        'message': 'may not all be set to false'
    }


def _has_material_terms(cycle: dict):
    materials = filter_list_term_type(cycle.get('inputs', []), TermTermType.MATERIAL)
    return len(materials) > 0 and list_sum(materials[0].get('value', [0])) > 0


def _has_terms(cycle: dict, term_ids: list, allow_no_value: bool = True):
    inputs = [input for input in cycle.get('inputs', []) if input.get('term', {}).get('@id') in term_ids]
    return len(inputs) > 0 if allow_no_value else any([len(input.get('value', [])) > 0 for input in inputs])


def _validate_material(cycle: dict):
    is_complete = cycle.get('completeness', {}).get(TermTermType.MATERIAL.value, False)
    fuel_ids = get_fuel_terms()
    return not is_complete or not _has_terms(cycle, fuel_ids, allow_no_value=True) or _has_material_terms(cycle) or {
        'level': 'error',
        'dataPath': f".completeness.{TermTermType.MATERIAL.value}",
        'message': 'must be set to false when specifying fuel use',
        'params': {
            'allowedValues': fuel_ids
        }
    }


def _validate_animalFeed(cycle: dict, site: dict):
    is_complete = cycle.get('completeness', {}).get('animalFeed', False)
    site_type = site.get('siteType')
    is_liveAnimal = is_live_animal_cycle(cycle)
    has_forage = _has_terms(cycle, get_forage_terms(), allow_no_value=False) if is_liveAnimal else False
    return not is_complete or site_type not in [
        SiteSiteType.CROPLAND.value,
        SiteSiteType.PERMANENT_PASTURE.value,
    ] or not is_liveAnimal or has_forage or {
        'level': 'error',
        'dataPath': '.completeness.animalFeed',
        'message': 'must have inputs representing the forage when set to true',
        'params': {
            'siteType': site_type
        }
    }


def validate_completeness(cycle: dict, site=None):
    data_completeness = cycle.get('completeness', {})
    return _filter_list_errors([
        _validate_all_values(data_completeness),
        _validate_material(cycle),
        _validate_cropland(data_completeness, site) if site else True,
        _validate_animalFeed(cycle, site) if site else True
    ])
