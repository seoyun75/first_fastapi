import pytest
from fastapi.testclient import TestClient
from pytest import Session
from domain.user import User
from repository.test_repository import TestRepository


def test_signup(client: TestClient,session) -> None:
    #given
    befor = TestRepository(session).count_users()
    #when
    response = client.post(
        "/users/signup",
        json={
            "user_id": "test_id",
            "password": "Test_password",
            "nickname": "nickname",
        },
    )
    data = response.json()
    
    #then
    assert befor + 1 == TestRepository(session).count_users()
    assert response.status_code == 201
    assert data["data"]["user_id"] == "test_id"
    assert data["data"]["password"] == "Test_password"


@pytest.fixture(name="createuser")
def create_user_data(session: Session) -> User:
    TestRepository(session).create_user(
        User(user_id="test_id", password="Test_password", nickname="nickname")
    )


def test_update_user(client: TestClient, createuser) -> None:
    #when
    response = client.patch(
        "/users/test_id",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
        json={"password": "update_password", "nickname": "update_nickname"},
    )
    data = response.json()["data"]
    #then
    assert response.status_code == 200
    assert data["password"] == "update_password"


def test_delete_user(client: TestClient, session: Session, createuser):
    #given
    befor = TestRepository(session).count_users()
    #when
    response = client.delete(
        "/users/test_id?password=Test_password",
        headers={"session-id": "b144e64a-d40a-43d8-a2ef-4c5039b87047"},
    )

    #then
    assert befor - 1 == TestRepository(session).count_users()
    assert response.status_code == 204
