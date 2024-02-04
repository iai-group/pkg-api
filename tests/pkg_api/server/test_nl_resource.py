"""Tests for the NL resource endpoint."""

from flask import Flask

# TODO: create mock for annotate method


def test_nl_resource_post_errors(client: Flask) -> None:
    """Tests POST with invalid data."""
    response = client.post("/nl", json={"owner_username": "test"})
    assert response.status_code == 400
    assert response.json == {"message": "Missing owner URI"}

    response = client.post(
        "/nl",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Missing query"}


def test_nl_resource_post_add_statement(client: Flask) -> None:
    """Tests POST with a valid add statement."""
    response = client.post(
        "/nl",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "query": "I like apples.",
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Statement added to your PKG."}


# def test_nl_resource_post_get_statement(client: Flask) -> None:
#     """Tests POST with a valid get statement."""
#     response = client.post(
#         "/nl",
#         json={
#             "owner_uri": "http://example.com/test",
#             "owner_username": "test",
#             "query": "What do I like?",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json == {"message": "GET not implemented."}


# def test_nl_resource_post_delete_statement(client: Flask) -> None:
#     """Tests POST with a valid delete statement."""
#     response = client.post(
#         "/nl",
#         json={
#             "owner_uri": "http://example.com/test",
#             "owner_username": "test",
#             "query": "Forget that I like apples.",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json == {"message": "DELETE not implemented."}
