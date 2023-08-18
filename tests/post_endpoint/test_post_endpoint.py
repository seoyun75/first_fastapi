from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Date

from post_fastapi.main import app
from repository.post_repository import PostRepository


def test_signup(client: TestClient):
    response = client.post(
        "/users/signup",
        json={"id": "Deadpond3", "password": "Aaaaaaaa", "nickname": "nickname"},
    )
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert data["data"]["id"] == "Deadpond3"
    assert data["data"]["password"] == "Aaaaaaaa"


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


def test_get_posts_(client: TestClient):
    response = client.get("/posts")
    assert response.status_code == 200
    # assert response.json() == {}


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
