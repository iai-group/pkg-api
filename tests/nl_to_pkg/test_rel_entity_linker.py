"""Tests for REL entity linker."""
import uuid
from unittest.mock import Mock, patch

import pytest

from pkg_api.core.annotation import Concept, PKGData, Triple, TripleElement
from pkg_api.core.pkg_types import URI
from pkg_api.nl_to_pkg.entity_linking.rel_entity_linking import RELEntityLinker


@pytest.fixture
def sample_pkg_data() -> PKGData:
    """Returns a test PKG data."""
    return PKGData(
        uuid.UUID("{123e4567-e89b-12d3-a456-426614174000}"),
        "Test statement",
        Triple(
            TripleElement("Test Subject"),
            TripleElement("Test Predicate"),
            TripleElement("Test Object"),
        ),
    )


@pytest.fixture
def rel_linker() -> RELEntityLinker:
    """Returns a RELLinker instance."""
    linker = RELEntityLinker()
    assert linker._api_url == "https://rel.cs.ru.nl/api"
    assert linker._template_uri == "https://en.wikipedia.org/wiki/{entity_name}"
    return linker


@patch("pkg_api.nl_to_pkg.entity_linking.rel_entity_linking.requests.post")
def test_link_entities_uri(
    mock_get: Mock, sample_pkg_data: PKGData, rel_linker: RELEntityLinker
) -> None:
    """Test the link_entities method."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        [0, 10, "Test Object", "Test_Object", 1, 1, "OBJ"]
    ]
    mock_get.return_value = mock_response
    annotated_pkg_data = rel_linker.link_entities(sample_pkg_data)

    assert annotated_pkg_data == sample_pkg_data
    assert isinstance(annotated_pkg_data.triple, Triple)
    assert isinstance(annotated_pkg_data.triple.object, TripleElement)
    assert annotated_pkg_data.triple.object.value == URI(
        "https://en.wikipedia.org/wiki/Test_Object"
    )


@patch("pkg_api.nl_to_pkg.entity_linking.rel_entity_linking.requests.post")
def test_link_entities_concept(
    mock_get: Mock, sample_pkg_data: PKGData, rel_linker: RELEntityLinker
) -> None:
    """Test the link_entities method."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [[0, 10, "Object", "Object", 1, 1, "OBJ"]]
    mock_get.return_value = mock_response
    annotated_pkg_data = rel_linker.link_entities(sample_pkg_data)

    assert annotated_pkg_data == sample_pkg_data
    assert isinstance(annotated_pkg_data.triple, Triple)
    assert isinstance(annotated_pkg_data.triple.object, TripleElement)
    assert annotated_pkg_data.triple.object.value == Concept(
        "Test Object",
        related_entities=[URI("https://en.wikipedia.org/wiki/Object")],
    )


def test_no_linked_entity(
    sample_pkg_data: PKGData, rel_linker: RELEntityLinker
) -> None:
    """Test the link_entities method."""
    annotated_pkg_data = rel_linker.link_entities(sample_pkg_data)
    assert annotated_pkg_data == sample_pkg_data
    assert isinstance(annotated_pkg_data.triple, Triple)
    assert isinstance(annotated_pkg_data.triple.object, TripleElement)
    assert annotated_pkg_data.triple.object.value == Concept("Test Object")
