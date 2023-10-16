import json
from typing import List
from functools import reduce
from datetime import datetime
from hestia_earth.schema import NodeType, TermTermType, UNIQUENESS_FIELDS
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import list_average, safe_parse_date, non_empty_list
from hestia_earth.utils.model import filter_list_term_type


def _next_error(values: list): return next((x for x in values if x is not True), True)


def _filter_list_errors(values: list, return_single=True):
    values = list(filter(lambda x: x is not True, values))
    return True if return_single and len(values) == 0 else (values[0] if return_single and len(values) == 1 else values)


def _list_except_item(values: list, item):
    try:
        idx = values.index(item)
        return values[:idx] + values[idx+1:]
    except ValueError:
        return values


def update_error_path(error: dict, key: str, index=None):
    path = f".{key}[{index}]{error.get('dataPath')}" if index is not None else f".{key}{error.get('dataPath')}"
    return {**error, **{'dataPath': path}}


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def hash_dict(value: dict): return json.dumps(value, sort_keys=True)


def _is_number(value): return value is not None and (isinstance(value, float) or isinstance(value, int))


def is_same_dict(a: dict, b: dict): return hash_dict(a) == hash_dict(b)


def _dict_without_key(a: dict, key: str):
    no_key = a.copy()
    if key in no_key:
        no_key.pop(key)
    return no_key


def _group_nodes(nodes: List[dict]):
    def group(groups: dict, node: dict):
        type = node.get('type')
        id = node.get('id')
        if type and id:
            groups[type] = groups.get(type, {})
            groups[type][id] = node
        return groups

    return reduce(group, nodes, {})


def _hash_nodes(nodes: List[dict]):
    def group(groups: dict, node: dict):
        type = node.get('type')
        id = node.get('id')
        if type and id:
            # store the hash of the node without the `id` for uniqueness check
            key = hash_dict(_dict_without_key(node, 'id'))
            groups[key] = groups.get(key, []) + [node]
        return groups

    return reduce(group, nodes, {})


def _get_by_key(x, y):
    return x if x is None else (
        x.get(y) if isinstance(x, dict) else list(map(lambda v: _get_dict_key(v, y), x))
    )


def _get_dict_key(value: dict, key: str): return reduce(lambda x, y: _get_by_key(x, y), key.split('.'), value)


def _value_range_error(value: int, minimum: int, maximum: int):
    return 'minimum' if minimum is not None and value < minimum else \
        'maximum' if maximum is not None and value > maximum else False


def _list_sum(values: list, prop: str): return sum(map(lambda v: _safe_cast(v.get(prop, 0), float, 0.0), values))


def _list_sum_terms(values: list, term_ids=[]):
    return sum([_value_average(node) for node in values if node.get('term', {}).get('@id') in term_ids])


def _compare_values(x, y):
    return next((True for item in x if item in y), False) if isinstance(x, list) and isinstance(y, list) else x == y


def _same_properties(value: dict, props: List[str]):
    def identical(test: dict):
        same_values = list(filter(lambda x: _compare_values(_get_dict_key(value, x), _get_dict_key(test, x)), props))
        return test if len(same_values) == len(props) else None
    return identical


def _value_average(node: dict, default=0, key='value'):
    try:
        value = node.get(key)
        return list_average(value, default) if isinstance(value, list) else (value or default)
    except Exception:
        return default


def term_id_prefix(term_id: str): return term_id.split('Kg')[0]


def _download_linked_node(node: dict):
    data = download_hestia(node.get('@id'), node.get('@type')) if node.get('@id') and node.get('@type') else None
    return data if (data or {}).get('@id') == node.get('@id') else None


def _find_linked_node(node_map: dict, node: dict):
    return node_map.get(node.get('type'), {}).get(node.get('id')) or _download_linked_node(node)


def _is_before_today(date: str): return safe_parse_date(date).date() <= datetime.now().date()


def _node_year(node: dict):
    date = node.get('endDate', node.get('startDate'))
    date = safe_parse_date(date) if date else None
    return date.year if date else None


def is_live_animal_cycle(cycle: dict):
    return any([
        len(filter_list_term_type(cycle.get('animals', []), [
            TermTermType.LIVEANIMAL,
            TermTermType.LIVEAQUATICSPECIES
        ])) > 0,
        len(filter_list_term_type(cycle.get('products', []), [
            TermTermType.LIVEANIMAL,
            TermTermType.LIVEAQUATICSPECIES
        ])) > 0
    ])


def _match_list_el(source: list, dest: list, key: str):
    src_values = non_empty_list([x.get(key) for x in source])
    dest_values = non_empty_list([x.get(key) for x in dest])
    return sorted(src_values) == sorted(dest_values)


def _match_el(source: dict, dest: dict, fields: list):
    def match(key: str):
        keys = key.split('.')
        is_list = len(keys) == 2 and (
            isinstance(source.get(keys[0]), list) or
            isinstance(dest.get(keys[0]), list)
        )
        return _match_list_el(
            _get_dict_key(source, keys[0]) or [],
            _get_dict_key(dest, keys[0]) or [],
            keys[1]
        ) if is_list else (_get_dict_key(dest, key) is None or _get_dict_key(source, key) == _get_dict_key(dest, key))

    return all(map(match, fields))


def is_same_product(p1: dict, p2: dict):
    keys = UNIQUENESS_FIELDS.get(NodeType.CYCLE.value).get('products', ['term.@id'])
    return _match_el(p1, p2, keys)


def find_by_product(node: dict, product: dict, list_key: str = 'products'):
    keys = UNIQUENESS_FIELDS.get(node.get('type', node.get('@type')), {}).get(list_key, ['term.@id'])
    products = node.get(list_key, [])
    return next((p for p in products if _match_el(p, product, keys)), None)


def get_term_lookup_value(term: dict, column: str):
    table_name = f"{term.get('termType')}.csv" if term else None
    value = get_table_value(
        download_lookup(table_name), 'termid', term.get('@id'), column_name(column)
    ) if table_name else None
    return value
