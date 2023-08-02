"""Tests for the PKG module."""
import pytest

from pkg_api.connector import RDFStore
from pkg_api.pkg import PKG


@pytest.fixture
def user_pkg() -> PKG:
    """Returns a PKG instance."""
    return PKG(
        "http://example.com/testuser", RDFStore.MEMORY, "tests/data/RDFStore"
    )


def test_add_fact(user_pkg: PKG) -> None:
    """Tests add_fact method."""
    user_pkg.add_fact(
        "http://example.com/testuser1",
        "http://example.org/likes",
        "http://example.org/pizza",
    )
    assert user_pkg.get_objects_from_facts(
        "http://example.com/testuser1", "http://example.org/likes"
    ) == ["http://example.org/pizza"]
    user_pkg.close()


def test_add_owner_fact(user_pkg) -> None:
    """Tests add_owner_fact method."""
    user_pkg.add_owner_fact(
        "http://example.org/likes",
        "http://example.org/pizza",
    )
    assert (
        user_pkg.get_owner_objects_from_facts("http://example.org/likes")[0]
        == "http://example.org/pizza"
    )
    user_pkg.close()


def test_remove_owner_fact(user_pkg) -> None:
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
    assert (
        user_pkg.get_owner_objects_from_facts("http://example.org/likes")[0]
        == "http://example.org/icecream"
    )
    assert (
        "http://example.org/pizza"
        not in user_pkg.get_owner_objects_from_facts("http://example.org/likes")
    )
    user_pkg.remove_owner_fact(
        "http://example.org/likes", "http://example.org/icecream"
    )
    assert (
        len(user_pkg.get_owner_objects_from_facts("http://example.org/likes"))
        == 0
    )
    user_pkg.close()
