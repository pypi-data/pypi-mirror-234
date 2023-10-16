from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import find_node, search

LIMIT = 10000


def get_fuel_terms():
    """
    Find all "liquid" `fuel` terms from the Glossary:
    - https://hestia.earth/glossary?termType=fuel&query=gasoline
    - https://hestia.earth/glossary?termType=fuel&query=petrol
    - https://hestia.earth/glossary?termType=fuel&query=diesel

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.FUEL.value
                    }
                }
            ],
            "should": [
                {
                    "regexp": {
                        "name": "*gasoline*"
                    }
                },
                {
                    "regexp": {
                        "name": "*petrol*"
                    }
                },
                {
                    "regexp": {
                        "name": "*diesel*"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_crop_residue_terms():
    terms = find_node(SchemaType.TERM, {'termType': TermTermType.CROPRESIDUE.value}, limit=LIMIT)
    return [term.get('@id') for term in terms if term.get('@id')]


def get_methodModels():
    terms = find_node(SchemaType.TERM, {'termType': TermTermType.MODEL.value}, limit=LIMIT)
    return [term.get('@id') for term in terms if term.get('@id')]


def get_forage_terms():
    """
    Find all "forage" `crop` or `forage` terms from the Glossary:
    - https://hestia.earth/glossary?termType=crop&query=forage
    - https://hestia.earth/glossary?termType=forage&query=forage

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                }
            ],
            "should": [
                {
                    "match": {
                        "termType.keyword": TermTermType.CROP.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.FORAGE.value
                    }
                },
                {
                    "match": {
                        "name": "forage"
                    }
                }
            ],
            "minimum_should_match": 2
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_rice_terms():
    """
    Find all "rice" `crop` terms from the Glossary:
    - https://hestia.earth/glossary?termType=crop&query=rice

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.CROP.value
                    }
                },
                {
                    "match": {
                        "name": "rice"
                    }
                }
            ]
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))
