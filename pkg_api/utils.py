"""Utils methods for the API.

The methods creates SPARQL queries to edit the PKG like adding/removing facts
or preferences. In practice, the preference is represented with a blank node
that links the subject, the object and the preference value (a float between -1
and 1).

For example:
    - Alice loves action movies with a preference of 0.8 is represented as:
    (:Alice pkg:preference _:blank)
    (_:blank pkg:entity :action_movies)
    (_:blank pkg:weight 0.8)
"""

from pkg_api.pkg_types import URI, SPARQLQuery

# Method to create RDF representation of the preference/fact
# Method to translate RDF to SPAQRL (OTTR)


def get_query_add_fact(
    subject: URI, predicate: URI, entity: URI
) -> SPARQLQuery:
    """Gets SPARQL query to add a fact.

    Args:
        subject: Subject of the fact.
        predicate: Predicate of the fact.
        entity: Entity of the fact.

    Returns:
        SPARQL query.
    """
    return f"""
        INSERT DATA {{
            <{subject}> <{predicate}> <{entity}> .
        }}
    """


def get_query_get_objects_from_facts(
    subject: URI, predicate: URI
) -> SPARQLQuery:
    """Gets SPARQL query to retrieve objects given subject and predicate.

    Args:
        subject: Subject of the fact.
        predicate: Predicate of the fact.

    Returns:
        SPARQL query.
    """
    return f"""
        SELECT ?object WHERE {{
            <{subject}> <{predicate}> ?object .
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
