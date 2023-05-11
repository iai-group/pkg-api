"""Utils methods for the API."""

from pkg_api.types import URI, SPARQLQuery

# Method to create RDF representation of the preference/fact
# Method to translate RDF to SPAQRL (OTTR)


def get_query_add_fact(who: URI, predicate: URI, entity: URI) -> SPARQLQuery:
    """Get SPARQL query to add a fact.

    Args:
        who: Who is adding the fact.
        predicate: Predicate of the fact.
        entity: Entity of the fact.

    Returns:
        SPARQL query.
    """
    return f"""
        INSERT DATA {{
            <{who}> <{predicate}> <{entity}> .
        }}
    """


def get_query_get_objects_from_facts(who: URI, predicate: URI) -> SPARQLQuery:
    """Get SPARQL query to get objects given subject and predicate.

    Args:
        who: Subject of the fact.
        predicate: Predicate of the fact.

    Returns:
        SPARQL query.
    """
    return f"""
        SELECT ?object WHERE {{
            <{who}> <{predicate}> ?object .
        }}
    """
