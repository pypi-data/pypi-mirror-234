from hestia_earth.schema import SiteSiteType
from hestia_earth.utils.tools import flatten

from hestia_earth.validation.gee import fetch_data_by_coordinates
from .shared import (
    validate_dates, validate_list_dates, validate_list_dates_format, validate_list_min_below_max,
    validate_list_min_max_lookup, validate_list_dates_after,
    validate_region_in_country, validate_country, validate_is_region, validate_coordinates, need_validate_coordinates,
    validate_area, need_validate_area, validate_list_term_percent, validate_linked_source_privacy,
    validate_list_date_lt_today, validate_date_lt_today, validate_boundary_area,
    validate_region_size, need_validate_region_size,
    validate_private_has_source, validate_list_value_between_min_max
)
from .infrastructure import validate_lifespan
from .measurement import (
    validate_soilTexture, validate_depths, validate_required_depths, validate_term_unique,
    validate_require_startDate_endDate, validate_with_models, validate_value_length
)
from .property import (
    validate_all as validate_properties
)
from .management import (
    validate_has_termTypes, validate_exists
)


INLAND_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.RIVER_OR_STREAM.value,
    SiteSiteType.LAKE.value,
    SiteSiteType.ANIMAL_HOUSING.value,
    SiteSiteType.AGRI_FOOD_PROCESSOR.value,
    SiteSiteType.FOOD_RETAILER.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value
]

SITE_TYPES_VALID_VALUES = {
    SiteSiteType.CROPLAND.value: [25, 35, 36],
    SiteSiteType.FOREST.value: [10, 20, 25]
}


def validate_site_dates(site: dict):
    return validate_dates(site) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_site_coordinates(site: dict):
    return need_validate_coordinates(site) and site.get('siteType') in INLAND_TYPES


def validate_siteType(site: dict):
    site_type = site.get('siteType')
    values = SITE_TYPES_VALID_VALUES.get(site_type, [])
    values_str = ', '.join(map(lambda v: str(v), values))
    coordinates = {
        'latitude': site.get('latitude'),
        'longitude': site.get('longitude')
    }
    collection = {
        'collection': 'MODIS/006/MCD12Q1',
        'band_name': 'LC_Prop2',
        'year': '2019'
    }

    def validate():
        value = fetch_data_by_coordinates(ee_type='raster_by_period', collection=collection, coordinates=coordinates)
        return value in values

    return len(values) == 0 or validate() or {
        'level': 'warning',
        'dataPath': '.siteType',
        'message': ' '.join([
            'The coordinates you have provided are not in a known',
            site_type,
            f"area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands {values_str})."
        ])
    }


def validate_site(site: dict, node_map: dict = {}):
    """
    Validates a single `Site`.

    Parameters
    ----------
    site : dict
        The `Site` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `Site`, which can be empty if no errors detected.
    """
    return [
        validate_site_dates(site),
        validate_date_lt_today(site, 'startDate'),
        validate_date_lt_today(site, 'endDate'),
        validate_linked_source_privacy(site, 'defaultSource', node_map),
        validate_private_has_source(site, 'defaultSource'),
        validate_siteType(site) if need_validate_coordinates(site) else True,
        validate_country(site) if 'country' in site else True,
        validate_is_region(site) if 'region' in site else True,
        validate_region_in_country(site) if 'region' in site else True,
        validate_coordinates(site) if validate_site_coordinates(site) else True,
        validate_area(site) if need_validate_area(site) else True,
        validate_boundary_area(site),
        validate_region_size(site) if need_validate_region_size(site) else True,
        validate_has_termTypes(site),
        validate_exists(site)
    ] + flatten(
        ([
            validate_list_dates(site, 'infrastructure'),
            validate_list_dates_format(site, 'infrastructure'),
            validate_list_date_lt_today(site, 'infrastructure', ['startDate', 'endDate']),
            validate_lifespan(site.get('infrastructure'))
        ] if 'infrastructure' in site else []) +
        ([
            validate_list_dates(site, 'measurements'),
            validate_list_dates_after(site, 'startDate', 'measurements', ['startDate', 'endDate', 'dates']),
            validate_list_dates_format(site, 'measurements'),
            validate_list_date_lt_today(site, 'measurements', ['startDate', 'endDate']),
            validate_list_min_below_max(site, 'measurements'),
            validate_list_value_between_min_max(site, 'measurements'),
            validate_list_min_max_lookup(site, 'measurements', 'value'),
            validate_list_min_max_lookup(site, 'measurements', 'min'),
            validate_list_min_max_lookup(site, 'measurements', 'max'),
            validate_list_term_percent(site, 'measurements'),
            validate_soilTexture(site.get('measurements')),
            validate_depths(site.get('measurements')),
            validate_required_depths(site, 'measurements'),
            validate_term_unique(site.get('measurements')),
            validate_properties(site, 'measurements'),
            validate_require_startDate_endDate(site, 'measurements'),
            validate_with_models(site, 'measurements'),
            validate_value_length(site, 'measurements')
        ] if len(site.get('measurements', [])) > 0 else [])
    )
