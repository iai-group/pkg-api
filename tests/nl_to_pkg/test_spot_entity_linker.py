from unittest.mock import MagicMock, patch

import pytest

from pkg_api.core.annotation import Concept, PKGData, Triple
from pkg_api.nl_to_pkg.entity_linking.spotlight_entity_linker import (
    SpotlightEntityLinker,
)


@pytest.fixture
def spotlight_entity_linker() -> SpotlightEntityLinker:
    """Fixture to create a SpotlightEntityLinker object."""
    mock_config = {
        "url": "test_url",
        "headers": {"accept": "application/json"},
        "params": {
            "confidence": 0.73,
            "support": 13,
        },
    }
    with patch(
        "pkg_api.nl_to_pkg.entity_linking.spotlight.load_yaml_config",
        return_value=mock_config,
    ):
        yield SpotlightEntityLinker()


@pytest.fixture
def pkg_data() -> PKGData:
    """Fixture to create a PKGData object."""
    return PKGData(
        "I dislike all movies with the actor Tom Cruise.",
        Triple(
            "I",
            Concept("dislike"),
            Concept("all movies with the actor Tom Cruise"),
        ),
    )


@pytest.fixture
def pkg_data_no_entities() -> PKGData:
    """Fixture to create a PKGData object with no entities."""
    return PKGData(
        "A random text with no entities.",
        Triple(
            "Subject",
            Concept("verb"),
            Concept("A random text with no entities."),
        ),
    )


@patch("requests.get")
def test_link_annotation_entities_valid_response(
    mock_requests_get: MagicMock,
    spotlight_entity_linker: SpotlightEntityLinker,
    pkg_data: PKGData,
) -> None:
    """Test linking entities with a valid API response."""
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        "Resources": [{"@URI": "http://dbpedia.org/resource/Tom_Cruise"}]
    }

    linked_data = spotlight_entity_linker.link_annotation_entities(pkg_data)
    assert linked_data.triple is not None
    assert linked_data.triple.object is not None
    assert len(linked_data.triple.object.related_entities) == 1
    assert (
        "http://dbpedia.org/resource/Tom_Cruise"
        in linked_data.triple.object.related_entities
    )


@patch("requests.get")
def test_link_annotation_entities_no_entities(
    mock_requests_get: MagicMock,
    spotlight_entity_linker: SpotlightEntityLinker,
    pkg_data_no_entities: PKGData,
) -> None:
    """Test linking entities when no entities are found."""
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {}

    linked_data = spotlight_entity_linker.link_annotation_entities(
        pkg_data_no_entities
    )
    assert linked_data.triple is not None
    assert linked_data.triple.object is not None
    assert len(linked_data.triple.object.related_entities) == 0


@patch("requests.get")
def test_link_annotation_entities_api_error(
    mock_requests_get: MagicMock,
    spotlight_entity_linker: SpotlightEntityLinker,
    pkg_data_no_entities: PKGData,
) -> None:
    """Test behavior when the API returns an error."""
    mock_requests_get.return_value.status_code = 500
    mock_requests_get.return_value.text = "Internal Server Error"
    spotlight_entity_linker = SpotlightEntityLinker()

    linked_data = spotlight_entity_linker.link_annotation_entities(
        pkg_data_no_entities
    )
    assert linked_data.triple is not None
    assert linked_data.triple.object is not None
    assert len(linked_data.triple.object.related_entities) == 0


@patch("requests.get")
def test_get_linker_response_request_parameters(
    mock_requests_get: MagicMock, spotlight_entity_linker: SpotlightEntityLinker
) -> None:
    """Test that _get_linker_response sends the correct request parameters."""
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        "Resources": [{"@URI": "http://dbpedia.org/resource/Tom_Cruise"}]
    }

    test_text = "Test text"
    response = spotlight_entity_linker._get_linker_response(test_text)

    mock_requests_get.assert_called_once_with(
        "test_url",
        headers={"accept": "application/json"},
        params={"confidence": 0.73, "support": 13, "text": test_text},
    )
    assert response == mock_requests_get.return_value.json.return_value
