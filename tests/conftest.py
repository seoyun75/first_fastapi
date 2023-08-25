from uuid import UUID

import pytest
from db import get_session
from fastapi import Header
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from tool.session import SessionData, verify_session

from post_fastapi.main import app
from tests.in_memory_test import InMemoryTest

# ---session id 생성/검즘
in_memory_test = InMemoryTest()
session_id = "b144e64a-d40a-43d8-a2ef-4c5039b87047"


def set_session_id(test_client):
    test_client.headers["session-id"] = session_id


@pytest.fixture(scope="session", name="session_data")
def create_test_session() -> None:
    in_memory_test.create(
        UUID("b144e64a-d40a-43d8-a2ef-4c5039b87047"), SessionData(user_id="test_id")
    )


def verify_test_session(session_id: UUID = Header()) -> SessionData:
    id = in_memory_test.read(session_id)

    return id


# ---db 설정
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session, session_data):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[verify_session] = verify_test_session

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
