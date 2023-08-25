from typing import List
import pytest
from api.post.dto.request import CreatePostRequest
from fastapi.testclient import TestClient
from pytest import Session
from domain.comment import Comment
from domain.post import Post
from repository.test_repository import TestRepository
from tests.conftest import set_session_id


def test_create_comment(client: TestClient, session_data):
    # given
    set_session_id(client)
    
    # when
    response = client.post(
        "/comments",
        json={"id": 11, "post_id": 11, "content": "create comment"},
    )

    # then
    data = response.json()["data"]

    assert response.status_code == 201
    assert data["id"] == 11 # 왜 타입이 int?
    assert data["post_id"] == 11
    assert data["content"] == "create comment"


@pytest.fixture(name="createcomment")
def create_post_data(session: Session, session_data)->Post:
    return TestRepository(session).create_comment({"id": 11, "post_id": 11, "content": "create comment", "user_id": "test_id"})


def test_get_comments(client: TestClient, createcomment: List[Post]):
    #when
    response = client.get("/comments/11?page=1"
                          )
    
    #then
    data = response.json()["data"]
    assert response.status_code == 200
    assert data[0]["id"] == createcomment[0].id
    assert data[0]["post_id"] == 11
    assert data[0]["content"] == "create comment"
    assert data[0]["user_id"] == "test_id"


def test_update_comment(client: TestClient, createcomment):
    # given
    set_session_id(client)
    
    #when
    response = client.patch(
        "/comments/11",
        json={"id":11, "post_id": 11, "content": "update content"},
    )
    
    #then
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["id"] == 11
    assert data["post_id"] == 11
    assert data["content"] == "update content"
    assert data["user_id"] == "test_id"


def test_delete_comment(client: TestClient, createcomment):
    # given
    set_session_id(client)
    
    #when
    response = client.delete(
        "/comments/11",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
    )

    #then
    assert response.status_code == 204
