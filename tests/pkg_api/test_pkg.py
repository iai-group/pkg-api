"""Tests for the pkg module."""
import pytest
import rdflib

from pkg_api.pkg import PKG


@pytest.fixture
def user_pkg():
    """Returns a PKG instance."""
    return PKG("http://example.com/testuser")


def test_add_owner_fact(user_pkg):
    """Tests add_owner_fact method."""
    user_pkg.add_owner_fact(
        "http://example.org/likes",
        "http://example.org/pizza",
    )
    assert user_pkg.get_owner_objects_from_facts(
        "http://example.org/likes"
    ).bindings[0]["object"] == rdflib.term.URIRef("http://example.org/pizza")
    user_pkg.close()


def test_remove_owner_fact(user_pkg):
    """Tests remove_owner_fact method."""
    user_pkg.add_owner_fact(
        "http://example.org/likes", "http://example.org/pizza"
    )
    user_pkg.add_owner_fact(
        "http://example.org/likes", "http://example.org/icecream"
    )
    user_pkg.remove_owner_fact(
        "http://example.org/likes", "http://example.org/pizza"
    )
    assert user_pkg.get_owner_objects_from_facts(
        "http://example.org/likes"
    ).bindings[0]["object"] == rdflib.term.URIRef("http://example.org/icecream")
    user_pkg.remove_owner_fact(
        "http://example.org/likes", "http://example.org/icecream"
    )
    assert (
        len(
            user_pkg.get_owner_objects_from_facts(
                "http://example.org/likes"
            ).bindings
        )
        == 0
    )
    user_pkg.close()
