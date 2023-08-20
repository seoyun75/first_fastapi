import pytest
from api.post.dto.request import CreatePostRequest
from fastapi.testclient import TestClient
from pytest import Session
from repository.test_repository import TestRepository


def test_create_post(client: TestClient, session_data):
    # given
    # when
    response = client.post(
        "/posts",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
        json={"id": 11, "title": "createtitle", "content": "create content"},
    )

    # then
    data = response.json()["data"]

    assert response.status_code == 201
    assert data["id"] == "11"
    assert data["title"] == "createtitle"
    assert data["content"] == "create content"
    assert data["user_id"] == "test_id"


def test_fail_create_post(client: TestClient):
    # when
    response = client.post(
        "/posts",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
        json={"id": 11, "title": "createtitle", "content": "create content"},
    )

    # then

    assert response.status_code == 400


@pytest.fixture(name="createpost")
def create_post_data(session: Session):
    TestRepository(session).create_post(
        {"id": 2, "title": "title", "content": "content", "user_id": "test_id"}
    )


def test_get_posts_(client: TestClient, createpost):
    response = client.get("/posts")
    assert response.status_code == 200


def test_update_post(client: TestClient):
    response = client.patch(
        "/posts/11",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
        json={"title": "update title", "content": "update content"},
    )
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["id"] == "11"
    assert data["title"] == "update title"
    assert data["content"] == "update content"
    assert data["user_id"] == "test_id"


def test_delete_post(client: TestClient):
    response = client.delete(
        "/posts/11",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
    )

    assert response.status_code == 204
