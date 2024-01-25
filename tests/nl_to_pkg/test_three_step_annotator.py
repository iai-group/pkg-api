from unittest.mock import patch

import pytest

from pkg_api.core.annotations import PreferenceAnnotation, TripleAnnotation
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
)


@pytest.fixture(autouse=True)
def mock_llm_connector():
    with patch(
        "pkg_api.nl_to_pkg.llm.llm_connector.LLMConnector.get_response"
    ) as mock_get_response:
        yield mock_get_response


@pytest.fixture(autouse=True)
def mock_prompt():
    with patch(
        "pkg_api.nl_to_pkg.llm.prompt.Prompt.get_prompt"
    ) as mock_get_prompt:
        yield mock_get_prompt


@pytest.fixture
def annotator():
    return ThreeStepStatementAnnotator()


def test_get_intent(mock_llm_connector, annotator):
    mock_llm_connector.return_value = "Answer: DELETE"

    intent = annotator._get_intent("Test statement")
    assert intent == Intent.DELETE


def test_get_triple(mock_llm_connector, annotator):
    mock_llm_connector.return_value = "Subject | Predicate | Object"

    triple = annotator._get_triple("Test statement")
    assert triple.subject == "Subject"
    assert triple.predicate == "Predicate"
    assert triple.object == "Object"


def test_get_triple_missing_value(mock_llm_connector, annotator):
    mock_llm_connector.return_value = "Subject | N/A | N/A"

    triple = annotator._get_triple("Test statement")
    assert triple.subject == "Subject"
    assert triple.predicate is None
    assert triple.object is None


def test_get_preference(mock_llm_connector, annotator):
    mock_llm_connector.return_value = "Preference is -1"

    preference = annotator._get_preference("Test statement", "Object")
    assert preference.topic == "Object"
    assert preference.weight == -1.0


def test_get_preference_invalid(mock_llm_connector, annotator):
    mock_llm_connector.return_value = "No preference"

    preference = annotator._get_preference("Test statement", "Object")
    assert preference is None


@patch(
    "pkg_api.nl_to_pkg.annotators.three_step_annotator."
    "ThreeStepStatementAnnotator._get_intent"
)
@patch(
    "pkg_api.nl_to_pkg.annotators.three_step_annotator."
    "ThreeStepStatementAnnotator._get_triple"
)
@patch(
    "pkg_api.nl_to_pkg.annotators.three_step_annotator."
    "ThreeStepStatementAnnotator._get_preference"
)
def test_get_annotations(
    mock_get_preference, mock_get_triple, mock_get_intent, annotator
):
    mock_get_intent.return_value = Intent.GET
    mock_get_triple.return_value = TripleAnnotation(
        "Subject", "Predicate", "Object"
    )
    mock_get_preference.return_value = PreferenceAnnotation("Object", 1.0)

    intent, pkg_data = annotator.get_annotations("Test statement")
    assert intent == Intent.GET
    assert pkg_data.triple.subject == "Subject"
    assert pkg_data.triple.predicate == "Predicate"
    assert pkg_data.triple.object == "Object"
    assert pkg_data.preference.topic == "Object"
    assert pkg_data.preference.weight == 1.0
