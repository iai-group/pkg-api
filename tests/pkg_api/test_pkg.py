"""Tests for the PKG module."""
import re

import pytest

from pkg_api.connector import RDFStore
from pkg_api.core.annotations import PKGData, Triple
from pkg_api.core.pkg_types import URI
from pkg_api.pkg import PKG


@pytest.fixture
def user_pkg() -> PKG:
    """Returns a PKG instance."""
    return PKG(
        "http://example.com/testuser", RDFStore.MEMORY, "tests/data/RDFStore"
    )


def test_add_statement(monkeypatch, user_pkg: PKG) -> None:
    """Tests adding a statement."""
    pkg_data = PKGData(
        statement="I live in Stavanger.",
        triple=Triple(
            URI("http://example.com/testuser"),
            "live",
            URI("https://dbpedia.org/page/Stavanger"),
        ),
        logging_data={"authoredBy": URI("http://example.com/testuser")},
    )

    expected_query = re.sub(
        r"\s+",
        " ",
        """INSERT DATA { _:st a rdf:Statement ; dc:description "I live in
     Stavanger." ; rdf:subject <http://example.com/testuser> ; rdf:predicate 
     "live" ; rdf:object <https://dbpedia.org/page/Stavanger> ; pav:authoredBy
     <http://example.com/testuser> . }""",
    ).strip()

    # Check that connector is called with the correct query
    def mock_execute_sparql_query(query: str) -> None:
        assert query == expected_query
        mock_execute_sparql_query.called = True

    monkeypatch.setattr(
        user_pkg._connector, "execute_sparql_query", mock_execute_sparql_query
    )
    user_pkg.add_statement(pkg_data)
    assert mock_execute_sparql_query.called
