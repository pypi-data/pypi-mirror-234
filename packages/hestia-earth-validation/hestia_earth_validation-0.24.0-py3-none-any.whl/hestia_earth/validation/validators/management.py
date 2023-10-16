from hestia_earth.schema import TermTermType, SiteSiteType
from hestia_earth.utils.model import filter_list_term_type

from hestia_earth.validation.utils import _filter_list_errors

_SITE_TYPE_TO_TERM_TYPES = {
    SiteSiteType.CROPLAND.value: [
        TermTermType.CROPRESIDUEMANAGEMENT,
        TermTermType.LANDUSEMANAGEMENT,
        TermTermType.TILLAGE,
        TermTermType.WATERREGIME
    ],
    SiteSiteType.PERMANENT_PASTURE.value: [
        TermTermType.LANDUSEMANAGEMENT,
        TermTermType.WATERREGIME
    ]
}


def validate_has_termType(site: dict, term_type: TermTermType):
    blank_nodes = filter_list_term_type(site.get('management', []), term_type)
    return len(blank_nodes) > 0 or {
        'level': 'warning',
        'dataPath': '.management',
        'message': 'should contain at least one management node',
        'params': {
            'termType': term_type.value
        }
    }


def validate_has_termTypes(site: dict):
    blank_nodes = site.get('management', [])
    term_types = _SITE_TYPE_TO_TERM_TYPES.get(site.get('siteType'), [])
    return len(term_types) == 0 or len(blank_nodes) == 0 or _filter_list_errors([
        validate_has_termType(site, term_type) for term_type in term_types
    ])


def validate_exists(site: dict):
    blank_nodes = site.get('management', [])
    term_types = _SITE_TYPE_TO_TERM_TYPES.get(site.get('siteType'), [])
    return len(term_types) == 0 or len(blank_nodes) > 0 or {
        'level': 'warning',
        'dataPath': '.management',
        'message': 'should contain at least one management node'
    }
