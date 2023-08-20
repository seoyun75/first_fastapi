from fastapi.testclient import TestClient
import pytest
from sqlmodel.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker
from db import get_session
from post_fastapi.main import app
from tool.session import SessionService, verify_session, verify_test_session


@pytest.fixture(name="session_data")
def session_data() -> None:
    session = SessionService()

    session.create_test_session()


# ---db 설정


@pytest.fixture(scope="session", name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///test.db", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[verify_session] = verify_test_session

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
