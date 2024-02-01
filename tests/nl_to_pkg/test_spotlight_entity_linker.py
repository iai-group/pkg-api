"""Tests the Spotlight entity linker class."""
from unittest.mock import Mock, patch

import pytest

from pkg_api.core.annotation import Concept, PKGData, Triple, TripleElement
from pkg_api.core.pkg_types import URI
from pkg_api.nl_to_pkg.entity_linking.spotlight_entity_linker import (
    SpotlightEntityLinker,
)


@pytest.fixture
def sample_pkg_data() -> PKGData:
    """Returns a test PKG data."""
    return PKGData(
        "Test statement",
        Triple(
            TripleElement("Test Subject"),
            TripleElement("Test Predicate"),
            TripleElement("Test Object"),
        ),
    )


@pytest.fixture
def linker() -> SpotlightEntityLinker:
    """Returns a SpotlightEntityLinker instance."""
    return SpotlightEntityLinker()


def test_spotlight_entity_linker_initialization(
    linker: SpotlightEntityLinker,
) -> None:
    """Test the initialization of the SpotlightEntityLinker."""
    assert "url" in linker._config
    assert "params" in linker._config
    assert "headers" in linker._config


@patch("pkg_api.nl_to_pkg.entity_linking.spotlight_entity_linker.requests.get")
def test_link_annotation_uri(
    mock_get: Mock, sample_pkg_data: PKGData, linker: SpotlightEntityLinker
) -> None:
    """Test the link_annotation_entities method."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Resources": [
            {
                "@surfaceForm": "Test Object",
                "@URI": "http://dbpedia.org/resource/Test_Object",
            }
        ]
    }
    mock_get.return_value = mock_response
    annotated_pkg_data = linker.link_annotation_entities(sample_pkg_data)

    assert annotated_pkg_data == sample_pkg_data
    assert isinstance(annotated_pkg_data.triple, Triple)
    assert isinstance(annotated_pkg_data.triple.object, TripleElement)
    assert isinstance(annotated_pkg_data.triple.object.value, URI)
    assert (
        annotated_pkg_data.triple.object.value
        == "http://dbpedia.org/resource/Test_Object"
    )


@patch("pkg_api.nl_to_pkg.entity_linking.spotlight_entity_linker.requests.get")
def test_link_annotation_concept(
    mock_get: Mock, sample_pkg_data: PKGData, linker: SpotlightEntityLinker
) -> None:
    """Test the link_annotation_entities method."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Resources": [
            {
                "@surfaceForm": "Object",
                "@URI": "http://dbpedia.org/resource/Object",
            }
        ]
    }
    mock_get.return_value = mock_response
    annotated_pkg_data = linker.link_annotation_entities(sample_pkg_data)

    assert isinstance(annotated_pkg_data.triple, Triple)
    assert isinstance(annotated_pkg_data.triple.object, TripleElement)
    assert isinstance(annotated_pkg_data.triple.object.value, Concept)
    assert len(annotated_pkg_data.triple.object.value.related_entities) == 1
    assert (
        annotated_pkg_data.triple.object.value.related_entities[0]
        == "http://dbpedia.org/resource/Object"
    )


def test_link_annotation_entities_no_change(
    sample_pkg_data: PKGData, linker: SpotlightEntityLinker
) -> None:
    """Test the link_annotation_entities method when no entities are linked."""
    original_pkg_data = sample_pkg_data
    annotated_pkg_data = linker.link_annotation_entities(original_pkg_data)

    assert annotated_pkg_data == original_pkg_data
