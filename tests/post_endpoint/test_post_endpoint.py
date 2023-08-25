import pytest
from fastapi.testclient import TestClient
from pytest import Session
from domain.post import Post
from repository.test_repository import TestRepository
from tests.conftest import session_id, set_session_id

@pytest.fixture()
def befor(session: Session):
    return TestRepository(session).count_posts()

def test_create_post(client: TestClient, session: Session, befor: int):
    # given
    set_session_id(client)

    # when
    response = client.post(
        "/posts",
        json={"id": 11, "title": "createtitle", "content": "create content"},
    )

    # then
    data = response.json()["data"]
    assert befor + 1 == TestRepository(session).count_posts()
    assert response.status_code == 201
    assert data["id"] == "11"
    assert data["title"] == "createtitle"
    assert data["content"] == "create content"
    assert data["user_id"] == "test_id"


def test_fail_create_post(client: TestClient, session: Session, createpost, befor: int):
    # given
    set_session_id(client)

    # when
    response = client.post(
        "/posts",
        json={"id": 11, "title": "createtitle", "content": "create content"},
    )

    # then
    assert response.status_code == 409
    assert befor == TestRepository(session).count_posts()


@pytest.fixture(name="createpost")
def create_post_data(session: Session):
    return TestRepository(session).create_post(
        {"id": 11, "title": "title", "content": "content", "user_id": "test_id"}
    )


def test_get_posts(client: TestClient, createpost:Post):
    # when
    response = client.get("/posts")

    # then
    data = response.json()["data"]
    assert response.status_code == 200
    assert len(data) != 0
    assert data[0]["id"] == str(createpost.id)
    assert data[0]["title"] == createpost.title
    assert data[0]["content"] == createpost.content
    assert data[0]["user_id"] == createpost.user_id


def test_update_post(
    client: TestClient,
    createpost,
):
    # given
    set_session_id(client)

    # when
    response = client.patch(
        "/posts/11",
        json={"title": "update title", "content": "update content"},
    )
    data = response.json()["data"]

    # then
    assert response.status_code == 200
    assert data["id"] == "11"
    assert data["title"] == "update title"
    assert data["content"] == "update content"
    assert data["user_id"] == "test_id"


def test_delete_post(client: TestClient, session: Session, createpost, befor: int):
    # given
    set_session_id(client)

    # when
    response = client.delete(
        "/posts/11",
        headers={"session-id": session_id},
    )

    # then
    assert response.status_code == 204
    assert befor - 1 == TestRepository(session).count_posts()