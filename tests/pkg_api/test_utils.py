"""Tests for utility methods."""


import re
from typing import Optional, Union

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


@pytest.fixture
def statement_representation() -> str:
    """Statement representation associated to pkg_data_example."""
    return """_:st a rdf:Statement ;
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
        pav:authoredOn "2024-26-01T11:41:00Z"^^xsd:dateTime ;
        pav:createdBy <http://example.com/my/I>
        .
    """


@pytest.fixture
def preference_representation() -> str:
    """Preference representation associated to pkg_data_example."""
    return """<http://example.com/my/I> wi:preference [
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
        ."""


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
    assert strip_string(
        utils._get_concept_representation(pkg_data_example.triple.object)
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


def test_get_preference_representation(
    pkg_data_example: PKGData, preference_representation: str
) -> None:
    """Tests _get_preference_representation method.

    Args:
        pkg_data_example: PKG data example.
        preference_representation: Expected preference representation.
    """
    assert strip_string(
        utils._get_preference_representation(pkg_data_example, "_:st")
    ) == strip_string(preference_representation)


def test_get_statement_representation(
    pkg_data_example: PKGData, statement_representation: str
) -> None:
    """Tests _get_statement_representation method.

    Args:
        pkg_data_example: PKG data example.
        statement_representation: Expected statement representation.
    """
    assert strip_string(
        utils._get_statement_representation(pkg_data_example, "_:st")
    ) == strip_string(statement_representation)


def test_get_query_for_add_statement(
    pkg_data_example: PKGData,
    statement_representation: str,
    preference_representation: str,
) -> None:
    """Tests _get_query_for_add_statement method.

    Args:
        pkg_data_example: PKG data example.
        statement_representation: Expected statement representation.
        preference_representation: Expected preference representation.
    """
    sparql_query = f"""INSERT DATA {{
        {statement_representation}

        {preference_representation}
    }}"""
    assert utils.get_query_for_add_statement(pkg_data_example) == strip_string(
        sparql_query
    )