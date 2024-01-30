"""Tests for PKG connector."""

import os

import pytest

from pkg_api.connector import Connector, RDFStore


@pytest.fixture
def pkg_connector() -> Connector:
    """Returns a connector instance."""
    return Connector(
        "http://example.com/testuser",
        RDFStore.MEMORY,
        "tests/data/RDFStore/testuser",
    )


def test_bind_namespaces(pkg_connector: Connector) -> None:
    """Tests binding namespaces."""
    graph_namespaces = dict(pkg_connector._graph.namespaces())
    assert len(graph_namespaces) >= 19
    assert (
        str(graph_namespaces["skos"]) == "http://www.w3.org/2004/02/skos/core#"
    )
    assert str(graph_namespaces["pkg"]) == "http://w3id.org/pkg/"


def test_save_graph(pkg_connector: Connector) -> None:
    """Tests saving graph."""
    pkg_connector.save_graph()
    assert os.path.exists("tests/data/RDFStore/testuser.ttl")


def test_save_grpah_exception() -> None:
    """Tests saving graph exception."""
    connector = Connector(
        "http://example.com/testuser",
        RDFStore.MEMORY,
        "non_existing_path",
    )
    with pytest.raises(FileNotFoundError):
        connector.save_graph()
