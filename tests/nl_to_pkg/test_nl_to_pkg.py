"""Test for pkg_api.nl_to_pkg.nl_to_pkg."""

from unittest.mock import Mock

import pytest

from pkg_api.core.annotations import (
    PKGData,
    PreferenceAnnotation,
    TripleAnnotation,
)
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.nl_to_pkg import NLtoPKG


@pytest.fixture
def statement():
    """Returns a test statement."""
    return "Subject, Predicate, Object"


@pytest.fixture
def statement_annotator_mock(statement):
    """Returns a mock statement annotator."""
    mock = Mock()
    intent = Intent.ADD
    triple = TripleAnnotation("Subject", "Predicate", "Object")
    preference = PreferenceAnnotation("Object", 1.0)
    mock.get_annotations.return_value = (
        intent,
        PKGData(statement, triple=triple, preference=preference),
    )
    return mock


@pytest.fixture
def entity_linker_mock():
    """Returns a mock entity linker."""
    mock = Mock()
    # Configure the mock to simulate entity linking
    # Update this with actual linked data you expect
    linked_triple = TripleAnnotation(
        "Linked Subject", "Linked Predicate", "Linked Object"
    )
    mock.link_annotation_entities.return_value = linked_triple
    return mock


@pytest.fixture
def nlp_to_pkg(statement_annotator_mock, entity_linker_mock):
    """Returns an NLtoPKG instance."""
    return NLtoPKG(statement_annotator_mock, entity_linker_mock)


def test_annotate_success(statement, nlp_to_pkg):
    """Tests that annotate returns the correct intent and annotations."""
    intent, pkg_data = nlp_to_pkg.annotate(statement)

    assert intent == Intent.ADD
    assert pkg_data.triple is not None
    assert pkg_data.triple.subject == "Linked Subject"


def test_annotate_no_triple(statement, nlp_to_pkg, statement_annotator_mock):
    """Tests that annotate returns the correct intent and annotations."""
    statement_annotator_mock.get_annotations.return_value = (
        Intent.DELETE,
        PKGData(statement, triple=None),
    )
    _, pkg_data = nlp_to_pkg.annotate(statement)

    assert pkg_data.triple is None
    assert pkg_data.preference is None


def test_annotate_with_preference_update(statement, nlp_to_pkg):
    """Tests that annotate returns the correct intent and annotations."""
    _, pkg_data = nlp_to_pkg.annotate(statement)

    assert pkg_data.preference.topic == "Linked Object"
