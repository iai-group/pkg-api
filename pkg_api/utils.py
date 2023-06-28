"""Utils methods for the API."""

from pkg_api.pkg_types import URI, SPARQLQuery

# Method to create RDF representation of the preference/fact
# Method to translate RDF to SPAQRL (OTTR)


def get_query_add_fact(who: URI, predicate: URI, entity: URI) -> SPARQLQuery:
    """Gets SPARQL query to add a fact.

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
    """Gets SPARQL query to retrieve objects given subject and predicate.

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


def get_query_remove_fact(
    subject: URI, predicate: URI, entity: URI
) -> SPARQLQuery:
    """Gets SPARQL query to remove a fact.

    Args:
        subject: Subject of the fact to remove.
        predicate: Predicate of the fact.
        entity: Entity of the fact.

    Returns:
        SPARQL query.
    """
    return f"""
         DELETE DATA {{
             <{subject}> <{predicate}> <{entity}> .
         }}
     """
