"""Utils methods for the API.

The methods creates SPARQL queries to edit the PKG like adding/removing
statements or preferences. See the PKG vocabulary for more information about
the properties of statements and preferences.

PKG vocabulary: https://iai-group.github.io/pkg-vocabulary/
"""

import dataclasses
import re
from typing import List

from pkg_api.core.annotations import Concept, PKGData
from pkg_api.core.pkg_types import URI, SPARQLQuery


def get_query_for_add_fact(
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


def get_query_for_get_objects_from_facts(
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


def get_query_for_set_preference(
    who: URI, entity: URI, preference: float
) -> SPARQLQuery:
    """Gets SPARQL query to set preference.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.
        preference: The preference value (a float between -1 and 1) for given
          entity.

    Returns:
        SPARQL query.
    """
    return f"""
        INSERT DATA {{
            <{who}> <preference>
            [ <entity> <{entity}> ;
                <weight> <{preference}> ]
        }}
    """


def get_query_for_update_preference(
    who: URI, entity: URI, old_preference: float, new_preference: float
) -> SPARQLQuery:
    """Gets SPARQL query to update preference value given subject and entity.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.
        old_preference: The old preference value for given entity.
        new_preference: The new preference value for given entity.

    Returns:
        SPARQL query.
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


def get_query_for_get_preference(who: URI, entity: URI) -> SPARQLQuery:
    """Gets SPARQL query to retrieve preference value given subject and entity.

    Args:
        who: Who is adding the fact.
        entity: Entity of the fact.

    Returns:
        SPARQL query.
    """
    return f"""
        SELECT ?pref {{
            <{who}> <preference>
            [ <entity> <{entity}> ;
                <weight> ?pref ]
        }}
    """


def get_query_for_remove_fact(
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


def get_query_for_add_statement(pkg_data: PKGData) -> SPARQLQuery:
    """Gets SPARQL query to add a statement.

    Args:
        pkg_data: PKG data associated to a statement.

    Returns:
        SPARQL query.
    """
    # Create a statement
    blank_node_id = "_:st"
    statement = f"""{blank_node_id} a rdf:Statement ;
        dc:description "{pkg_data.statement}"@en ; """

    # Add triple annotation
    for field in dataclasses.fields(pkg_data.triple):
        property = field.name
        annotation = getattr(pkg_data.triple, property)
        if isinstance(annotation, URI):
            statement += f"rdf:{property} <{annotation}> ; "
        elif isinstance(annotation, Concept):
            concept = _get_concept_representation(annotation)
            statement += f"rdf:{property} {concept} ; "
        elif annotation:
            statement += f'rdf:{property} "{annotation}" ; '

    # Add logging data
    # Time related data
    for property in ["authoredOn", "createdOn"]:
        if pkg_data.logging_data.get(property):
            statement += f"""
            pav:{property} "{pkg_data.logging_data[property]}"^^xsd:dateTime ;
            """
    # Author related data
    for property in ["createdBy", "authoredBy"]:
        if pkg_data.logging_data.get(property):
            statement += (
                f"pav:{property} <{pkg_data.logging_data[property]}> ; "
            )

    statement += " . "
    # Add preference
    if pkg_data.preference:
        preference_topic = (
            f"<{pkg_data.preference.topic}>"
            if isinstance(pkg_data.preference.topic, URI)
            else _get_concept_representation(pkg_data.preference.topic)
        )
        subject = (
            f"<{pkg_data.triple.subject}>"
            if pkg_data.triple.subject
            else f'"{pkg_data.triple.subject}"'
        )
        preference = f"""{subject} wi:preference
            [
                pav:derivedFrom {blank_node_id} ;
                wi:topic {preference_topic} ;
                wo:weight [
                    wo:weight_value {pkg_data.preference.weight} ;
                    wo:scale pkg:StandardScale
                ]
            ] .
        """

    query = f"""
        INSERT DATA {{
            {statement}

            {preference}
        }}
    """
    return re.sub(r";\s*(?=[]\.])", "", query)


def _get_concept_representation(concept: Concept) -> str:
    """Gets the representation of a concept given an annotation.

    Args:
        concept: Concept.

    Returns:
        Representation of the concept.
    """
    concept_template = """[
        a skos:Concept ; dc:description "{description}" ;
        {related_entities}
        {broader_entities}
        {narrower_entities}
    ]"""
    related_entities = (
        f"skos:related {_get_uri_list(concept.related_entities)} ; "
        if concept.related_entities
        else ""
    )
    broader_entities = (
        f"skos:broader {_get_uri_list(concept.broader_entities)} ; "
        if concept.broader_entities
        else ""
    )
    narrower_entities = (
        f"skos:narrower {_get_uri_list(concept.narrower_entities)} ; "
        if concept.narrower_entities
        else ""
    )
    return concept_template.format(
        description=concept.description,
        related_entities=related_entities,
        broader_entities=broader_entities,
        narrower_entities=narrower_entities,
    )


def _get_uri_list(entities: List[URI]) -> str:
    """Gets a list of URIs as a string for SPARQL queries.

    Args:
        entities: List of URIs.

    Returns:
        String with URIs separated by commas.
    """
    return ", ".join([f"<{ent}>" for ent in entities])
