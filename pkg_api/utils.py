"""Utils methods for the API.

The methods creates SPARQL queries to edit the PKG like adding/removing facts
or preferences. In practice, the preference is represented with a blank node
that links the subject, the object and the preference value (a float between -1
and 1).

For example:
    - 'Bob like Titanic with a preference of 0.75' is represented as:
    (:Bob pkg:preference _:blank)
    (_:blank pkg:entity :titanic)
    (_:blank pkg:weight 0.75)
    - 'Alice loves action movies with a preference of 0.8' is represented as:
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

  
def get_query_set_preference(who: URI, entity: URI, preference: float):
    """Gets SPARQL query to set preference.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.
        preference: The preference value (a float between -1 and 1) for given
          entity.
    """
    return f"""
        INSERT DATA {{
            <{who}> <preference>
            [ <entity> <{entity}> ;
                <weight> <{preference}> ]
        }}
    """


def get_query_update_preference(
    who: URI, entity: URI, old_preference: float, new_preference: float
):
    """Gets SPARQL query to update preference value given subject and entity.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.
        old_preference: The old preference value for given entity.
        new_preference: The new preference value for given entity.
    """
    return f"""
        DELETE {{ ?x <weight> <{old_preference}> }}
        INSERT {{ ?x <weight> <{new_preference}> }}
        WHERE  {{
            <{who}> <preference> ?x .
            ?x <entity> <{entity}> .
            ?x <weight> ?old_preference .
        }}
    """


def get_query_get_preference(who: URI, entity: URI):
    """Gets SPARQL query to retrieve preference value given subject and entity.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.
    """
    return f"""
        SELECT ?pref {{
            <{who}> <preference>
            [ <entity> <{entity}> ;
                <weight> ?pref ]
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
