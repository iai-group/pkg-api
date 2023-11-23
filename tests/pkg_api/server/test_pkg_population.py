"""Tests for the PKG population endpoints."""
from pkg_api.connector import RDFStore
from pkg_api.pkg import PKG


def test_population_post_body_error(client) -> None:
    """Tests POST endpoint with invalid body."""
    response = client.post("/population", json={})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Invalid request body."}


def test_population_post_query_error(client) -> None:
    """Tests POST endpoint with invalid query."""
    response = client.post(
        "/population",
        json={
            "owner_uri": "http://example.org/pkg/test_user",
            "owner_username": "test_user",
            "query": "invalid query",
        },
    )
    assert response.status_code == 500
    assert response.get_json() == {
        "message": "The query string should be in the following format:"
        " Type: [fact|preference] Subject: [me|owner|URI] Predicate: [URI]"
        " Object: [URI|Literal] Preference: [preference]."
        " Some fields are optional, but the order must be preserved."
    }

    response = client.post(
        "/population",
        json={
            "owner_uri": "http://example.org/pkg/test_user",
            "owner_username": "test_user",
            "query": "Type: fact Subject: me",
        },
    )
    assert response.status_code == 500
    assert response.get_json() == {
        "message": "The query string should be in the following format:"
        " Type: [fact|preference] Subject: [me|owner|URI] Predicate: [URI]"
        " Object: [URI|Literal] Preference: [preference]."
        " Some fields are optional, but the order must be preserved."
    }


def test_population_post_fact(client) -> None:
    """Tests POST endpoint with a fact."""
    response = client.post(
        "/population",
        json={
            "owner_uri": "http://example.org/pkg/test_user",
            "owner_username": "test_user",
            "query": "Type: fact Subject: me Predicate: "
            "http://example.org/pkg/play Object: http://example.org/pkg/guitar",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Your PKG was modified."}

    pkg = PKG(
        "http://example.org/pkg/test_user",
        RDFStore.MEMORY,
        "data/RDFStore/test_user",
    )
    objects = pkg.get_owner_objects_from_facts("http://example.org/pkg/play")
    assert len(objects) == 1
    assert objects[0] == "http://example.org/pkg/guitar"
    pkg.close()


def test_population_post_preference(client) -> None:
    """Tests POST endpoint with a preference."""
    response = client.post(
        "/population",
        json={
            "owner_uri": "http://example.org/pkg/test_user",
            "owner_username": "test_user",
            "query": "Type: preference Subject: me Object: "
            "http://example.org/pkg/green Preference: 0.8",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Your PKG was modified."}

    pkg = PKG(
        "http://example.org/pkg/test_user",
        RDFStore.MEMORY,
        "data/RDFStore/test_user",
    )
    assert pkg.get_owner_preference("http://example.org/pkg/green") == 0.8
    pkg.close()


def test_population_delete_body_error(client) -> None:
    """Tests DELETE endpoint with invalid body."""
    response = client.delete("/population", json={"data": ""})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Invalid request body."}


def test_population_delete_preference(client) -> None:
    """Tests DELETE endpoint with a preference."""
    response = client.delete(
        "/population",
        json={
            "owner_uri": "http://example.org/pkg/test_user",
            "owner_username": "test_user",
            "query": "Type: preference Subject: me Object: "
            "http://example.org/pkg/green",
        },
    )
    assert response.status_code == 500
    assert response.get_json() == {
        "message": "Cannot find an appropriate method."
    }


def test_population_delete_fact(client) -> None:
    """Tests DELETE endpoint with a fact."""
    response = client.delete(
        "/population",
        json={
            "owner_uri": "http://example.org/pkg/test_user",
            "owner_username": "test_user",
            "query": "Type: fact Subject: me Predicate: "
            "http://example.org/pkg/play Object: http://example.org/pkg/guitar",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Your PKG was modified."}

    pkg = PKG(
        "http://example.org/pkg/test_user",
        RDFStore.MEMORY,
        "data/RDFStore/test_user",
    )
    objects = pkg.get_owner_objects_from_facts("http://example.org/pkg/play")
    assert len(objects) == 0
    pkg.close()
