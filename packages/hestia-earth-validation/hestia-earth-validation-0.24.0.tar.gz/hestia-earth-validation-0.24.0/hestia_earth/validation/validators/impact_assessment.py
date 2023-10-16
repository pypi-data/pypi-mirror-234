from hestia_earth.utils.tools import flatten

from hestia_earth.validation.utils import _find_linked_node, find_by_product
from .aggregated_shared import (
    validate_quality_score_min
)
from .shared import (
    validate_list_min_below_max, validate_region_in_country, validate_country, validate_is_region,
    validate_list_term_percent, validate_linked_source_privacy, validate_date_lt_today,
    validate_list_model, validate_private_has_source, validate_list_value_between_min_max, is_date_equal
)
from .indicator import validate_characterisedIndicator_model, validate_landTransformation


def validate_linked_cycle_product(impact_assessment: dict, cycle: dict):
    product = impact_assessment.get('product', {})
    has_product = find_by_product(cycle, product) is not None
    return has_product or {
        'level': 'error',
        'dataPath': '.product',
        'message': 'should be included in the cycle products',
        'params': {
            'product': product.get('term', {}),
            'node': {
                'type': 'Cycle',
                'id': cycle.get('id', cycle.get('@id'))
            }
        }
    }


def validate_linked_cycle_endDate(impact_assessment: dict, cycle: dict):
    key = 'endDate'
    return is_date_equal(impact_assessment.get(key), cycle.get(key), True) or {
        'level': 'error',
        'dataPath': f".{key}",
        'message': f"must be equal to the Cycle {key}"
    }


def validate_impact_assessment(impact_assessment: dict, node_map: dict = {}):
    """
    Validates a single `ImpactAssessment`.

    Parameters
    ----------
    impact_assessment : dict
        The `ImpactAssessment` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `ImpactAssessment`, which can be empty if no errors detected.
    """
    cycle = _find_linked_node(node_map, impact_assessment.get('cycle', {}))
    return [
        validate_date_lt_today(impact_assessment, 'startDate'),
        validate_date_lt_today(impact_assessment, 'endDate'),
        validate_linked_source_privacy(impact_assessment, 'source', node_map),
        validate_private_has_source(impact_assessment, 'source'),
        validate_country(impact_assessment) if 'country' in impact_assessment else True,
        validate_is_region(impact_assessment) if 'region' in impact_assessment else True,
        validate_region_in_country(impact_assessment) if 'region' in impact_assessment else True,
        validate_linked_cycle_product(impact_assessment, cycle) if cycle else True,
        validate_linked_cycle_endDate(impact_assessment, cycle) if cycle else True
    ] + flatten(
        ([
            validate_list_min_below_max(impact_assessment, 'emissionsResourceUse'),
            validate_list_value_between_min_max(impact_assessment, 'emissionsResourceUse'),
            validate_list_term_percent(impact_assessment, 'emissionsResourceUse'),
            validate_characterisedIndicator_model(impact_assessment, 'emissionsResourceUse'),
            validate_landTransformation(impact_assessment, 'emissionsResourceUse')
        ] if len(impact_assessment.get('emissionsResourceUse', [])) > 0 else []) +
        ([
            validate_list_min_below_max(impact_assessment, 'impacts'),
            validate_list_value_between_min_max(impact_assessment, 'impacts'),
            validate_list_term_percent(impact_assessment, 'impacts'),
            validate_list_model(impact_assessment, 'impacts'),
            validate_characterisedIndicator_model(impact_assessment, 'impacts')
        ] if len(impact_assessment.get('impacts', [])) > 0 else []) +
        ([
            validate_list_min_below_max(impact_assessment, 'endpoints'),
            validate_list_value_between_min_max(impact_assessment, 'endpoints'),
            validate_list_term_percent(impact_assessment, 'endpoints')
        ] if len(impact_assessment.get('endpoints', [])) > 0 else [])
    )


def validate_impact_assessment_aggregated(impact_assessment: dict, node_map: dict = {}):
    return flatten([
        validate_quality_score_min(impact_assessment)
    ])
