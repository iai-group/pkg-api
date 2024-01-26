"""Tests for utility methods."""


import re

import pytest

from pkg_api import utils
from pkg_api.core.annotations import Concept, PKGData, Preference, Triple
from pkg_api.core.pkg_types import URI


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
    _object = Concept(
        description="all movies with the actor Tom Cruise",
        related_entities=[
            URI("https://schema.org/actor"),
            URI("http://dbpedia.org/resource/Tom_Cruise"),
        ],
        broader_entities=[URI("https://schema.org/Movie")],
        narrower_entities=[URI("https://schema.org/Action")],
    )
    return PKGData(
        statement="I dislike all movies with the actor Tom Cruise.",
        triple=Triple(
            subject=URI("http://example.com/my/I"),
            predicate=Concept(description="dislike"),
            object=_object,
        ),
        preference=Preference(
            topic=_object,
            weight=-1.0,
        ),
        logging_data={
            "authoredOn": "2024-26-01T11:41:00Z",
            "createdBy": "http://example.com/my/I",
        },
    )


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
    ) == strip_string('[ a skos:Concept ; dc:description "concept" ; ]')


def test_get_concept_representation(pkg_data_example: PKGData) -> None:
    """Tests _get_concept_representation method for PKGData."""
    assert strip_string(
        utils._get_concept_representation(pkg_data_example.triple.object)
    ) == strip_string(
        """[ a skos:Concept ; dc:description "all movies with
         the actor Tom Cruise" ; skos:related <https://schema.org/actor>,
         <http://dbpedia.org/resource/Tom_Cruise> ; skos:broader
         <https://schema.org/Movie> ; skos:narrower <https://schema.org/Action>
         ; ]"""
    )


def test_get_query_for_add_statement(pkg_data_example: PKGData) -> None:
    """Tests _get_query_for_add_statement method."""
    sparql_query = """INSERT DATA {
        _:st a rdf:Statement ;
        dc:description "I dislike all movies with the actor Tom Cruise."@en ;
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
        pav:authoredOn "2024-26-01T11:41:00Z"^^xsd:dateTime ;
        pav:createdBy <http://example.com/my/I>
        .

        <http://example.com/my/I> wi:preference [
            pav:derivedFrom _:st ;
            wi:topic [
                a skos:Concept ; dc:description "all movies with the actor Tom
                Cruise" ; skos:related <https://schema.org/actor>,
                <http://dbpedia.org/resource/Tom_Cruise> ;
                skos:broader <https://schema.org/Movie> ;
                skos:narrower <https://schema.org/Action>
            ] ;
            wo:weight [
                wo:weight_value -1.0 ;
                wo:scale pkg:StandardScale
            ]
        ]
        .
    }"""
    assert strip_string(
        utils.get_query_for_add_statement(pkg_data_example)
    ) == strip_string(sparql_query)
