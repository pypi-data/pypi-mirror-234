from hestia_earth.schema import TermTermType


def validate_has_animals(cycle: dict):
    has_liveAnimal = any(
        p for p in cycle.get('products', []) if p.get('term', {}).get('termType') == TermTermType.LIVEANIMAL.value
    )
    has_animals = len(cycle.get('animals', [])) > 0
    return not has_liveAnimal or has_animals or {
        'level': 'warning',
        'dataPath': '',
        'message': 'should specify the herd composition'
    }
