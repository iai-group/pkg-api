"""Tests for NL to PKG class."""

import uuid
from unittest.mock import Mock

import pytest

from pkg_api.core.annotation import PKGData, Preference, Triple, TripleElement
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.nl_to_pkg import NLtoPKG


@pytest.fixture
def statement() -> str:
    """Returns a test statement."""
    return "Subject, Predicate, Object"


@pytest.fixture
def statement_annotator_mock(statement: str) -> Mock:
    """Returns a mock statement annotator."""
    mock = Mock()
    intent = Intent.ADD
    triple_object = TripleElement("Object")
    triple = Triple(
        TripleElement("Subject"),
        TripleElement("Predicate"),
        triple_object,
    )
    preference = Preference(triple_object, 1.0)
    mock.get_annotations.return_value = (
        intent,
        PKGData(uuid.uuid1(), statement, triple=triple, preference=preference),
    )
    return mock


@pytest.fixture
def entity_linker_mock() -> Mock:
    """Returns a mock entity linker."""
    mock = Mock()

    def link_annotation_side_effect(*args, **kwargs):
        """Returns a pkg data with linked triple and preference."""
        # Check if 'triple' argument is None
        pkg_data = args[0] if len(args) == 1 else kwargs["pkg_data"]
        if pkg_data.triple is None:
            return PKGData(uuid.uuid1(), "Test", triple=None, preference=None)
        else:
            # Default behavior for other cases
            pkg_data.triple.subject.value = "Linked Subject"
            pkg_data.triple.predicate.value = "Linked Predicate"
            pkg_data.triple.object.value = "Linked Object"
            return pkg_data

    mock.link_entities.side_effect = link_annotation_side_effect
    return mock


@pytest.fixture
def nl_to_pkg(
    statement_annotator_mock: Mock,
    entity_linker_mock: Mock,
) -> NLtoPKG:
    """Returns an NLtoPKG instance."""
    return NLtoPKG(statement_annotator_mock, entity_linker_mock)


def test_annotate_success(statement: str, nl_to_pkg: NLtoPKG) -> None:
    """Tests that annotate returns the correct intent and annotations."""
    intent, pkg_data = nl_to_pkg.annotate(statement)

    assert intent == Intent.ADD
    assert pkg_data.triple is not None
    assert pkg_data.triple.subject == TripleElement("Subject", "Linked Subject")


def test_annotate_no_triple(
    statement: str,
    nl_to_pkg: NLtoPKG,
    statement_annotator_mock: Mock,
) -> None:
    """Tests that annotate returns the correct intent and annotations."""
    statement_annotator_mock.get_annotations.return_value = (
        Intent.DELETE,
        PKGData(uuid.uuid1(), statement, triple=None),
    )
    _, pkg_data = nl_to_pkg.annotate(statement)

    assert pkg_data.triple is None
    assert pkg_data.preference is None


def test_annotate_with_preference_update(
    statement: str, nl_to_pkg: NLtoPKG
) -> None:
    """Tests that annotate returns the correct intent and annotations."""
    _, pkg_data = nl_to_pkg.annotate(statement)

    assert pkg_data.preference is not None
    assert pkg_data.preference.topic == TripleElement("Object", "Linked Object")
