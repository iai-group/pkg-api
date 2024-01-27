"""Utils methods for the API.

The methods creates SPARQL queries to edit the PKG like adding/removing
statements or preferences. See the PKG vocabulary for more information about
the properties of statements and preferences.

PKG vocabulary: https://iai-group.github.io/pkg-vocabulary/
"""

import dataclasses
import re
from typing import List, Union

from pkg_api.core.annotations import Concept, PKGData
from pkg_api.core.pkg_types import URI, SPARQLQuery


def _get_uri_list(entities: List[URI]) -> str:
    """Gets a list of URIs as a string for SPARQL queries.

    Args:
        entities: List of URIs.

    Returns:
        String with URIs separated by commas.
    """
    return ", ".join([f"<{ent}>" for ent in entities])


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


def _get_preference_representation(
    pkg_data: PKGData, blank_node_id: str
) -> str:
    """Gets the representation of a preference given a statement.

    Args:
        pkg_data: PKG data associated to a statement.
        blank_node_id: Blank node ID of the statement.

    Returns:
        Representation of the preference.
    """
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

    return f"""{subject} wi:preference
            [
                pav:derivedFrom {blank_node_id} ;
                wi:topic {preference_topic} ;
                wo:weight [
                    wo:weight_value {pkg_data.preference.weight} ;
                    wo:scale pkg:StandardScale
                ]
            ] .
        """


def get_query_for_get_preference(
    who: Union[str, URI], topic: Union[URI, Concept, str]
) -> SPARQLQuery:
    """Gets SPARQL query to retrieve preference value given a subject and topic.

    Args:
        who: Subject.
        topic: Topic.

    Returns:
        SPARQL query.
    """
    subject = f"<{who}>" if isinstance(who, URI) else f'"{who}"'
    preference_topic = ""
    if isinstance(topic, URI):
        preference_topic = f"<{topic}>"
    elif isinstance(topic, Concept):
        preference_topic = _get_concept_representation(topic)
    else:
        preference_topic = f'"{topic}"'

    return f"""
        SELECT ?weight
        WHERE {{
            {subject} wi:preference [
                wi:topic {preference_topic} ;
                wo:weight [
                    wo:weight_value ?weight ;
                    wo:scale pkg:StandardScale
                ]
            ]
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
        dc:description "{pkg_data.statement}" ; """

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

    # Create a preference
    preference = ""
    if pkg_data.preference:
        preference = _get_preference_representation(pkg_data, blank_node_id)

    query = f"""
        INSERT DATA {{
            {statement}

            {preference}
        }}
    """

    # Cleaning up the query
    query = re.sub(r";\s*(?=[]\.])", "", query).strip()
    query = re.sub(r"\s+", " ", query)
    return query
