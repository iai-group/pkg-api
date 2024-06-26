"""Utils methods for the API.

The methods creates SPARQL queries to edit the PKG like adding/removing
statements or preferences. See the PKG vocabulary for more information
about the properties of statements and preferences.

PKG vocabulary:
https://iai-group.github.io/pkg-vocabulary/
"""

import dataclasses
import re
from typing import List, Optional, Union

from pkg_api.core.namespaces import PKGPrefixes
from pkg_api.core.pkg_types import (
    URI,
    Concept,
    PKGData,
    SPARQLQuery,
    Triple,
    TripleElement,
)

_SPARQL_STATEMENT_VARIABLE = "?statement"


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
        description=re.sub(r'"', r"\"", concept.description),
        related_entities=related_entities,
        broader_entities=broader_entities,
        narrower_entities=narrower_entities,
    )
    return _clean_sparql_representation(representation)


def get_query_for_conditioned_get_preference(
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

    query = f"""
        SELECT ?weight
        WHERE {{
            {subject} wi:preference [
                wi:topic {preference_topic} ;
                wo:weight [
                    wo:weight_value ?weight ;
                    wo:scale pkg:StandardScale
                ]
            ] .
        }}
    """
    return _clean_sparql_representation(query)


def _get_statement_representation(
    pkg_data: PKGData, statement_node_id: str
) -> str:
    """Gets the representation of a statement given a PKG data.

    Args:
        pkg_data: PKG data associated to a statement.
        statement_node_id: Node ID of the statement.

    Returns:
        Representation of the statement.
    """
    raw_statement = re.sub(r'"', r"\"", pkg_data.statement)
    statement = f"""{statement_node_id} a rdf:Statement ;
        dc:description "{raw_statement}" ; """

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
    statement_node_id = get_statement_node_id(pkg_data)
    # Create a statement
    statement = _get_statement_representation(pkg_data, statement_node_id)

    query = f"""
        INSERT DATA {{
            {statement}
        }}
    """

    # Cleaning up the query
    return _clean_sparql_representation(query)


def get_query_for_add_preference(pkg_data: PKGData) -> SPARQLQuery:
    """Gets SPARQL query to add a preference.

    Args:
        pkg_data: PKG data associated to a statement.

    Returns:
        SPARQL query.
    """
    statement_node_id = get_statement_node_id(pkg_data)

    if pkg_data.preference is None:
        return ""

    query = f"""
        INSERT {{
            ?subject wi:preference [
                pav:derivedFrom {_SPARQL_STATEMENT_VARIABLE} ;
                wi:topic ?object ; wo:weight [
                    wo:weight_value "{pkg_data.preference.weight}"^^xsd:decimal;
                    wo:scale pkg:StandardScale
                ]
            ] .
        }}
        WHERE {{
            {statement_node_id} a rdf:Statement ;
            rdf:subject ?subject; rdf:object ?object .
            BIND({statement_node_id} AS {_SPARQL_STATEMENT_VARIABLE})
        }}
    """

    # Cleaning up the query
    return _clean_sparql_representation(query)


def get_statement_node_id(pkg_data: PKGData) -> str:
    """Gets the statement node ID based UUID."""
    return f"{PKGPrefixes.EX.name.lower()}:{pkg_data.id}"


def get_query_for_get_statements(pkg_data: PKGData) -> SPARQLQuery:
    """Gets SPARQL query to get statements.

    This query is strict and only look for statements that exactly match the
    PKG data.

    Args:
        pkg_data: PKG data.

    Returns:
        SPARQL query.
    """
    statement_representation = _get_statement_representation(
        pkg_data, _SPARQL_STATEMENT_VARIABLE
    )
    query = f"""
        SELECT {_SPARQL_STATEMENT_VARIABLE}
        WHERE {{
            {statement_representation}
        }}
    """

    # Cleaning up the query
    return _clean_sparql_representation(query)


def get_query_for_conditional_get_statements(triple: Triple) -> SPARQLQuery:
    """Gets SPARQL query to get statements given conditions in the triple.

    This query looks for statements that match the conditions in the triple.
    For example, if the subject is URI("http://example.com/testuser"), the
    query will return all statements with that subject.

    Args:
        triple: Triple with conditions.

    Returns:
        SPARQL query.
    """
    conditions = []
    for field in dataclasses.fields(triple):
        # Loop through the fields of the triple (subject, predicate, object), if
        # defined add a condition on it to the query. For example, if predicate
        # is like, the query will return all statements with that predicate.
        property = f"rdf:{field.name}"
        annotation = getattr(triple, field.name)
        annotation = annotation.value if annotation else None
        if not annotation:
            continue
        value = _get_property_representation(annotation)
        conditions.append(f"{_SPARQL_STATEMENT_VARIABLE} {property} {value} .")

    query = f"""
        SELECT {_SPARQL_STATEMENT_VARIABLE}
        WHERE {{
            {" ".join(conditions)}
        }}
    """

    # Cleaning up the query
    return _clean_sparql_representation(query)


def get_query_for_remove_preference(pkg_data: PKGData) -> SPARQLQuery:
    """Gets SPARQL query to remove a preference.

    Args:
        pkg_data: PKG data associated to a statement.

    Returns:
        SPARQL query.
    """
    statement = _get_statement_representation(
        pkg_data, _SPARQL_STATEMENT_VARIABLE
    )
    # Remove statement description from conditions
    statement = re.sub(r'dc:description "[^"]+" ;', "", statement)

    query = f"""
        DELETE {{
            ?preference ?p ?o .
            ?subject wi:preference ?preference .
        }}
        WHERE {{
            {statement}
            ?subject wi:preference ?preference .
            ?preference pav:derivedFrom {_SPARQL_STATEMENT_VARIABLE} .
            ?preference ?p ?o .
        }}
    """

    # Cleaning up the query
    return _clean_sparql_representation(query)


def get_query_for_remove_statement(pkg_data: PKGData) -> SPARQLQuery:
    """Gets SPARQL query to remove a statement.

    Note that if a preference is derived from the statement, it is also removed.

    Args:
        pkg_data: PKG data associated to a statement.

    Returns:
        SPARQL query.
    """
    statement_representation = _get_statement_representation(
        pkg_data, _SPARQL_STATEMENT_VARIABLE
    )
    # Remove statement description from conditions
    statement_representation = re.sub(
        r'dc:description "[^"]+" ;', "", statement_representation
    )

    query = f"""
        DELETE {{
            {_SPARQL_STATEMENT_VARIABLE} ?p ?o .
            ?preference ?pp ?op .
        }}
        WHERE {{
            {statement_representation}
            {_SPARQL_STATEMENT_VARIABLE} ?p ?o .
            OPTIONAL {{
                ?preference pav:derivedFrom {_SPARQL_STATEMENT_VARIABLE} .
                ?preference ?pp ?op .
            }}
        }}
    """

    # Cleaning up the query
    return _clean_sparql_representation(query)


def get_queries_for_remove_cleanup() -> List[SPARQLQuery]:
    """Gets SPARQL queries to delete dangling concepts and weight scales.

    Returns:
        List of SPARQL queries.
    """
    query_delete_concepts = """
        DELETE {
            ?concept ?p ?o .
        } WHERE {
            ?concept a skos:Concept .
            ?concept ?p ?o .
            FILTER NOT EXISTS { ?_1 ?_2 ?concept . }
        }
    """
    query_delete_concepts = _clean_sparql_representation(query_delete_concepts)
    query_delete_scales = """
        DELETE {
            ?x ?p ?o .
        } WHERE {
            ?x wo:scale ?_3 .
            ?x ?p ?o .
            FILTER NOT EXISTS { ?_1 ?_2 ?x . }
        }
    """
    query_delete_scales = _clean_sparql_representation(query_delete_scales)
    return [query_delete_concepts, query_delete_scales]
