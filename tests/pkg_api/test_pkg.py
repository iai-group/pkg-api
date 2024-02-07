"""Tests for the PKG module."""
import re
import uuid

import pytest

from pkg_api.connector import RDFStore
from pkg_api.core.annotation import Concept, PKGData, Preference, Triple, TripleElement
from pkg_api.core.pkg_types import URI
from pkg_api.pkg import PKG
from pkg_api.utils import get_statement_node_id


@pytest.fixture
def user_pkg() -> PKG:
    """Returns a PKG instance."""
    pkg = PKG(
        URI("http://example.com/testuser"),
        RDFStore.MEMORY,
        "tests/data/RDFStore",
    )
    assert pkg.owner_uri == URI("http://example.com/testuser")
    return pkg


@pytest.fixture
def statement() -> PKGData:
    """Returns a statement."""
    return PKGData(
        id=uuid.UUID("{abcac10b-58cc-4372-a567-0e02b2c3d479}"),
        statement="I live in Stavanger.",
        triple=Triple(
            TripleElement("I", URI("http://example.com/testuser")),
            TripleElement("live", "live"),
            TripleElement(
                "Stavanger", URI("https://dbpedia.org/page/Stavanger")
            ),
        ),
        logging_data={
            "authoredBy": URI("http://example.com/testuser"),
            "authoredOn": "2024-02-05T13:54:32",
        },
    )


@pytest.fixture
def statement_with_concept() -> PKGData:
    """Returns a statement."""
    _object = TripleElement(
        "movies directed by Steven Spielberg",
        Concept(
            description="movies directed by Steven Spielberg",
            related_entities=[URI("https://dbpedia.org/page/Steven_Spielberg")],
        ),
    )

    return PKGData(
        id=uuid.UUID("{f47ac10b-58cc-4372-a567-0e02b2c3d479}"),
        statement="I like movies directed by Steven Spielberg.",
        triple=Triple(
            TripleElement("I", URI("http://example.com/testuser")),
            TripleElement("like", Concept(description="like")),
            _object,
        ),
        preference=Preference(_object, 1.0),
        logging_data={
            "authoredBy": URI("http://example.com/testuser"),
            "authoredOn": "2024-02-05T13:54:32",
        },
    )


@pytest.fixture
def retrieved_statement_with_concept() -> PKGData:
    """Returns a statement retrieved from the PKG."""
    return PKGData(
        id=uuid.UUID("{f47ac10b-58cc-4372-a567-0e02b2c3d479}"),
        statement="I like movies directed by Steven Spielberg.",
        triple=Triple(
            TripleElement("", URI("http://example.com/testuser")),
            TripleElement("like", Concept(description="like")),
            TripleElement(
                "movies directed by Steven Spielberg",
                Concept(
                    description="movies directed by Steven Spielberg",
                    related_entities=[
                        URI("https://dbpedia.org/page/Steven_Spielberg")
                    ],
                ),
            ),
        ),
        preference=None,
        logging_data={
            "authoredBy": URI("http://example.com/testuser"),
            "authoredOn": "2024-02-05T13:54:32",
        },
    )


def test_add_statement(
    monkeypatch: pytest.MonkeyPatch, user_pkg: PKG, statement: PKGData
) -> None:
    """Tests adding a statement."""
    expected_query = re.sub(
        r"\s+",
        " ",
        f"""INSERT DATA {{ {get_statement_node_id(statement)} a rdf:Statement ;
        dc:description "I live in Stavanger." ;
        rdf:subject <http://example.com/testuser> ; rdf:predicate "live" ;
        rdf:object <https://dbpedia.org/page/Stavanger> ;
        pav:authoredOn "2024-02-05T13:54:32"^^xsd:dateTime ;
        pav:authoredBy <http://example.com/testuser> . }}""",
    ).strip()

    # Check that connector is called with the correct query
    def mock_execute_sparql_update(query: str) -> None:
        """Mock function for execute_sparql_update."""
        assert query == expected_query
        mock_execute_sparql_update.called = True

    monkeypatch.setattr(
        user_pkg._connector,
        "execute_sparql_update",
        mock_execute_sparql_update,
    )
    user_pkg.add_statement(statement)
    assert mock_execute_sparql_update.called


def test_get_statements(
    user_pkg: PKG, statement: PKGData, statement_with_concept: PKGData
) -> None:
    """Tests getting statements strictly matching PKG data."""
    user_pkg.add_statement(statement)
    user_pkg.add_statement(statement_with_concept)

    statements = user_pkg.get_statements(statement_with_concept)
    assert len(statements) == 1

    # get_statements does not return the preference
    statement_with_concept.preference = None
    assert statements[0] == statement_with_concept


def test_get_statements_with_triple_conditions(
    user_pkg: PKG, statement_with_concept: PKGData
) -> None:
    """Tests getting statements with triple conditions."""
    user_pkg.add_statement(statement_with_concept)
    user_pkg.add_statement(
        PKGData(
            statement="I like movies.",
            triple=Triple(
                URI("http://example.com/testuser"),
                Concept(description="like"),
                Concept(description="movies"),
            ),
        )
    )

    statements = user_pkg.get_statements(
        PKGData(
            statement="Get me everything I like.",
            triple=Triple(
                predicate=Concept(description="like"),
            ),
        ),
        triple_conditioned=True,
    )
    assert len(statements) == 2
    statement_with_concept.preference = None
    assert statement_with_concept in statements


def test_remove_statement(user_pkg: PKG, statement: PKGData) -> None:
    """Tests removing a statement."""
    user_pkg.add_statement(statement)
    statements = user_pkg.get_statements(statement)
    assert len(statements) == 1

    user_pkg.remove_statement(statement)
    statements = user_pkg.get_statements(statement)
    assert len(statements) == 0
