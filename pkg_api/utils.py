"""Utils methods for the API."""

from pkg_api.types import URI, SPARQLQuery

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
    # return f"""
    #     INSERT DATA {{
    #         <{who}> <preference> _:blank .
    #         _:blank <entity> <{entity}> .
    #         _:blank <weight> <{preference}> .
    #     }}
    # """

def get_query_update_preference(who: URI, entity: URI, old_preference: float, new_preference: float):
    """Gets SPARQL query to retrieve preference value given subject and entity.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.
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
    # return f"""
    #     SELECT ?who ?entity ?pref WHERE {{
    #         ?who <preference> ?x .
    #         ?x <entity> ?entity .
    #         ?x <weight> ?pref 
    #     }}
    # """

def select(who: URI, entity: URI):
    return f"""
        SELECT ?pref WHERE {{
            <{who}> <preference>
            [ <entity> <{entity}> ;
                <weight> ?pref ]
        }}
    """
    # return f"""
    #     SELECT ?who ?entity ?pref {{
    #         ?who <preference>
    #         [ <entity> ?entity ;
    #             <weight> ?pref ]
    #     }}
    # """