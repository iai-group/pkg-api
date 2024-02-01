"""Utils methods for the API.

The methods creates SPARQL queries to edit the PKG like adding/removing
statements or preferences. See the PKG vocabulary for more information about
the properties of statements and preferences.

PKG vocabulary: https://iai-group.github.io/pkg-vocabulary/
"""

import dataclasses
import re
from typing import List, Optional, Union

from pkg_api.core.annotation import Concept, PKGData, TripleElement
from pkg_api.core.pkg_types import URI, SPARQLQuery


def _clean_sparql_representation(sparql: str) -> str:
    """Cleans a SPARQL representation.

    Removes unwanted semicolons and new lines.

    Args:
        sparql: SPARQL representation.

    Returns:
        Cleaned SPARQL representation.
    """
    sparql = re.sub(r";\s*(?=[]\.])", "", sparql).strip()
    sparql = re.sub(r"\s+", " ", sparql)
    return sparql


def _get_uri_list(entities: List[URI]) -> str:
    """Gets a list of URIs as a string for SPARQL queries.

    Args:
        entities: List of URIs.

    Returns:
        String with URIs separated by commas.
    """
    return ", ".join([f"<{ent}>" for ent in entities])


def _get_property_representation(
    value: Union[URI, Concept, str], property: Optional[str] = None
) -> str:
    """Gets the representation for a property.

    Args:
        value: Value of the property.
        property: Property name. Defaults to None.

    Returns:
        Representation of the property.
    """
    representation = f"{property}" if property else ""
    if isinstance(value, URI):
        # The value is an URI, e.g., https://dbpedia.org/page/Tom_Cruise.
        return f"{representation} <{value}>"
    elif isinstance(value, Concept):
        # The value is a concept, e.g., Concept(description="movies with Tom
        # Cruise", related_entities=["https://dbpedia.org/page/Tom_Cruise"]).
        return f"{representation} {_get_concept_representation(value)}"

    # The value is a literal, e.g., "dislike".
    return f'{representation} "{value}"'


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
    representation = concept_template.format(
        description=concept.description,
        related_entities=related_entities,
        broader_entities=broader_entities,
        narrower_entities=narrower_entities,
    )
    return _clean_sparql_representation(representation)


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
    if pkg_data.preference is None or pkg_data.preference.topic.value is None:
        return ""

    preference_topic = _get_property_representation(
        pkg_data.preference.topic.value
    )

    if (
        pkg_data.triple is None
        or pkg_data.triple.subject is None
        or pkg_data.triple.subject.value is None
    ):
        return ""

    subject = _get_property_representation(pkg_data.triple.subject.value)

    representation = f"""{subject} wi:preference
            [
                pav:derivedFrom {blank_node_id} ;
                wi:topic {preference_topic} ;
                wo:weight [
                    wo:weight_value {pkg_data.preference.weight} ;
                    wo:scale pkg:StandardScale
                ]
            ] .
        """
    return _clean_sparql_representation(representation)


def get_query_for_get_preference(
    who: Union[str, URI], topic: Union[URI, Concept, str]
) -> SPARQLQuery:
    """Gets query to retrieve preference value given a subject and topic.

    Args:
        who: Subject.
        topic: Topic of the preference. Usually, the object of the statement.

    Returns:
        SPARQL query.
    """
    subject = _get_property_representation(who)
    preference_topic = _get_property_representation(topic)

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


def _get_statement_representation(pkg_data: PKGData, blank_node_id: str) -> str:
    """Gets the representation of a statement given a PKG data.

    Args:
        pkg_data: PKG data associated to a statement.
        blank_node_id: Blank node ID of the statement.

    Returns:
        Representation of the statement.
    """
    statement = f"""{blank_node_id} a rdf:Statement ;
        dc:description "{pkg_data.statement}" ; """

    # Add triple annotation
    if pkg_data.triple is not None:
        for field in dataclasses.fields(pkg_data.triple):
            property = f"rdf:{field.name}"
            annotation: TripleElement = getattr(pkg_data.triple, field.name)
            if annotation is None or annotation.value is None:
                continue
            statement += (
                f"{_get_property_representation(annotation.value, property)} ; "
            )

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
    return _clean_sparql_representation(statement)


def get_query_for_add_statement(pkg_data: PKGData) -> SPARQLQuery:
    """Gets SPARQL query to add a statement.

    Args:
        pkg_data: PKG data associated to a statement.

    Returns:
        SPARQL query.
    """
    blank_node_id = "_:st"
    # Create a statement
    statement = _get_statement_representation(pkg_data, blank_node_id)

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
    return _clean_sparql_representation(query)
