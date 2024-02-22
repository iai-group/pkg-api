"""Tests for utility methods."""

import re
import uuid
from typing import Optional, Union

import pytest

from pkg_api import utils
from pkg_api.core.pkg_types import (
    URI,
    Concept,
    PKGData,
    Preference,
    Triple,
    TripleElement,
)


def strip_string(string: str) -> str:
    """Strips string of multiple spaces and new lines.

    Args:
        string: String to strip.

    Returns:
        Stripped string.
    """
    return re.sub(r"\s+", " ", string).strip()


@pytest.fixture
def pkg_data_example() -> PKGData:
    """Returns PKG data for a given statement."""
    _object = TripleElement(
        "all movies with the actor Tom Cruise",
        Concept(
            description="all movies with the actor Tom Cruise",
            related_entities=[
                URI("https://schema.org/actor"),
                URI("http://dbpedia.org/resource/Tom_Cruise"),
            ],
            broader_entities=[URI("https://schema.org/Movie")],
            narrower_entities=[URI("https://schema.org/Action")],
        ),
    )
    return PKGData(
        id=uuid.UUID("{abcac10b-58cc-4372-a567-0e02b2c3d479}"),
        statement="I dislike all movies with the actor Tom Cruise.",
        triple=Triple(
            subject=TripleElement("I", URI("http://example.com/my/I")),
            predicate=TripleElement("dislike", Concept(description="dislike")),
            object=_object,
        ),
        preference=Preference(
            topic=_object,
            weight=-1.0,
        ),
        logging_data={
            "authoredOn": "2024-26-01T11:41:00",
            "createdBy": "http://example.com/my/I",
            "authoredBy": "http://example.com/my/I",
        },
    )


@pytest.fixture
def statement_representation(pkg_data_example: PKGData) -> str:
    """Statement representation associated to pkg_data_example."""
    return f"""{utils.get_statement_node_id(pkg_data_example)} a rdf:Statement ;
        dc:description "I dislike all movies with the actor Tom Cruise." ;
        rdf:subject <http://example.com/my/I> ;
        rdf:predicate [ a skos:Concept ; dc:description "dislike" ] ;
        rdf:object
        [
            a skos:Concept ; dc:description "all movies with the actor Tom
            Cruise" ; skos:related <https://schema.org/actor>,
            <http://dbpedia.org/resource/Tom_Cruise> ;
            skos:broader <https://schema.org/Movie> ;
            skos:narrower <https://schema.org/Action>
        ] ;
        pav:authoredOn "2024-26-01T11:41:00"^^xsd:dateTime ;
        pav:createdBy <http://example.com/my/I> ;
        pav:authoredBy <http://example.com/my/I>
        .
    """


@pytest.mark.parametrize(
    "uris, expected",
    [
        ([URI("https://example.org/uri")], "<https://example.org/uri>"),
        (
            [URI("https://example.org/uri1"), URI("https://example.org/uri2")],
            "<https://example.org/uri1>, <https://example.org/uri2>",
        ),
    ],
)
def test_get_uris_representation(uris: list, expected: str) -> None:
    """Tests _get_uri_list method.

    Args:
        uris: URIs to test.
        expected: Expected representation.
    """
    assert utils._get_uri_list(uris) == expected


def test_get_concept_representation_string() -> None:
    """Tests _get_concept_representation method for string."""
    concept = Concept(description="concept")
    assert strip_string(
        utils._get_concept_representation(concept).strip()
    ) == strip_string('[ a skos:Concept ; dc:description "concept" ]')


def test_get_concept_representation(pkg_data_example: PKGData) -> None:
    """Tests _get_concept_representation method for PKGData."""
    assert isinstance(pkg_data_example.triple, Triple)
    assert isinstance(pkg_data_example.triple.object, TripleElement)
    assert isinstance(pkg_data_example.triple.object.value, Concept)
    assert strip_string(
        utils._get_concept_representation(pkg_data_example.triple.object.value)
    ) == strip_string(
        """[ a skos:Concept ; dc:description "all movies with
         the actor Tom Cruise" ; skos:related <https://schema.org/actor>,
         <http://dbpedia.org/resource/Tom_Cruise> ; skos:broader
         <https://schema.org/Movie> ; skos:narrower <https://schema.org/Action>
         ]"""
    )


@pytest.mark.parametrize(
    "value, property, expected",
    [
        (
            URI("https://example.org/uri"),
            "rdf:subject",
            "rdf:subject <https://example.org/uri>",
        ),
        ("literal", "rdf:predicate", 'rdf:predicate "literal"'),
        (
            Concept(
                description="concept",
                related_entities=[URI("https://example.org/uri")],
            ),
            "object",
            'object [ a skos:Concept ; dc:description "concept" ; skos:related '
            "<https://example.org/uri> ]",
        ),
        ("literal", None, ' "literal"'),
    ],
)
def test_get_property_representation(
    value: Union[URI, Concept, str], property: Optional[str], expected: str
) -> None:
    """Tests _get_property_representation method.

    Args:
        value: Value to test.
        property: Property to test.
        expected: Expected representation.
    """
    assert strip_string(
        utils._get_property_representation(value, property)
    ) == strip_string(expected)


def test_get_statement_representation(
    pkg_data_example: PKGData, statement_representation: str
) -> None:
    """Tests _get_statement_representation method.

    Args:
        pkg_data_example: PKG data example.
        statement_representation: Expected statement representation.
    """
    statement_node_id = utils.get_statement_node_id(pkg_data_example)
    assert strip_string(
        utils._get_statement_representation(pkg_data_example, statement_node_id)
    ) == strip_string(statement_representation)


def test_get_query_for_add_statement(
    pkg_data_example: PKGData,
    statement_representation: str,
) -> None:
    """Tests _get_query_for_add_statement method.

    Args:
        pkg_data_example: PKG data example.
        statement_representation: Statement representation.
    """
    sparql_query = f"""INSERT DATA {{
        {statement_representation}
    }}"""
    assert utils.get_query_for_add_statement(pkg_data_example) == strip_string(
        sparql_query
    )


def test_get_query_for_add_preference(
    pkg_data_example: PKGData,
) -> None:
    """Tests _get_query_for_add_preference method.

    Args:
        pkg_data_example: PKG data example.
    """
    sparql_query = """
        INSERT {
            ?subject wi:preference [
                pav:derivedFrom ?statement ;
                wi:topic ?object ; wo:weight [
                    wo:weight_value "-1.0"^^xsd:decimal;
                    wo:scale pkg:StandardScale
                ]
            ] .
        }
        WHERE {
            ex:abcac10b-58cc-4372-a567-0e02b2c3d479 a rdf:Statement ;
            rdf:subject ?subject; rdf:object ?object .
            BIND(ex:abcac10b-58cc-4372-a567-0e02b2c3d479 AS ?statement)
        }
    """
    assert utils.get_query_for_add_preference(pkg_data_example) == strip_string(
        sparql_query
    )


def test_get_query_for_conditioned_get_preference(
    pkg_data_example: PKGData,
) -> None:
    """Tests get_query_for_conditioned_get_preference method."""
    expected_query = """
        SELECT ?weight
        WHERE {
            <http://example.com/my/I> wi:preference [
                wi:topic [
                    a skos:Concept ;
                    dc:description "all movies with the actor Tom Cruise" ;
                    skos:related <https://schema.org/actor>,
                    <http://dbpedia.org/resource/Tom_Cruise> ;
                    skos:broader <https://schema.org/Movie> ;
                    skos:narrower <https://schema.org/Action>
                ] ;
                wo:weight [
                    wo:weight_value ?weight ;
                    wo:scale pkg:StandardScale
                ]
            ] .
        }
    """
    assert utils.get_query_for_conditioned_get_preference(
        pkg_data_example.triple.subject.value,
        pkg_data_example.triple.object.value,
    ) == strip_string(expected_query)


def test_get_query_for_get_statements(
    pkg_data_example: PKGData, statement_representation: str
) -> None:
    """Tests get_query_for_get_statements method.

    Args:
        pkg_data_example: PKG data example.
        statement_representation: Statement representation.
    """
    statement_node_id = utils.get_statement_node_id(pkg_data_example)
    sparql_query = f"""SELECT ?statement
        WHERE {{
            {statement_representation.replace(statement_node_id, "?statement")}
        }}"""

    assert utils.get_query_for_get_statements(pkg_data_example) == strip_string(
        sparql_query
    )


def test_get_query_for_conditional_get_statements(
    pkg_data_example: PKGData,
) -> None:
    """Tests get_query_for_conditional_get_statements method."""
    expected_query = """
        SELECT ?statement
        WHERE {
            ?statement rdf:subject <http://example.com/my/I> .
            ?statement rdf:predicate [
                a skos:Concept ; dc:description "dislike"
            ] .
            ?statement rdf:object [
                a skos:Concept ;
                dc:description "all movies with the actor Tom Cruise" ;
                skos:related <https://schema.org/actor>,
                <http://dbpedia.org/resource/Tom_Cruise> ;
                skos:broader <https://schema.org/Movie> ;
                skos:narrower <https://schema.org/Action>
            ] .
        }
    """
    assert utils.get_query_for_conditional_get_statements(
        pkg_data_example.triple
    ) == strip_string(expected_query)


def test_get_query_for_remove_statement(
    pkg_data_example: PKGData, statement_representation: str
) -> None:
    """Tests get_query_for_remove_statement method.

    Args:
        pkg_data_example: PKG data example.
        statement_representation: Statement representation.
    """
    statement_node_id = utils.get_statement_node_id(pkg_data_example)
    statement_representation = statement_representation.replace(
        statement_node_id, "?statement"
    )
    statement_representation = re.sub(
        r'dc:description "[^"]+" ;', "", statement_representation
    )
    sparql_query = f"""
        DELETE {{
            ?statement ?p ?o .
            ?preference ?pp ?op .
        }}
        WHERE {{
            {statement_representation}
            ?statement ?p ?o .
            OPTIONAL {{
                ?preference pav:derivedFrom ?statement .
                ?preference ?pp ?op .
            }}
        }}
    """

    assert utils.get_query_for_remove_statement(
        pkg_data_example
    ) == strip_string(sparql_query)


def test_get_query_for_remove_preference(
    pkg_data_example: PKGData, statement_representation: str
) -> None:
    """Tests get_query_for_remove_preference method."""
    statement_node_id = utils.get_statement_node_id(pkg_data_example)
    statement_representation = statement_representation.replace(
        statement_node_id, "?statement"
    )
    statement_representation = re.sub(
        r'dc:description "[^"]+" ;', "", statement_representation
    )

    sparql_query = f"""
        DELETE {{
            ?preference ?p ?o .
            ?subject wi:preference ?preference .
        }}
        WHERE {{
            {statement_representation}
            ?subject wi:preference ?preference .
            ?preference pav:derivedFrom ?statement .
            ?preference ?p ?o .
        }}
    """
    assert utils.get_query_for_remove_preference(
        pkg_data_example
    ) == strip_string(sparql_query)
