from uuid import UUID, uuid4

from fastapi import Depends, Header, HTTPException, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from pydantic import BaseModel
from tool.in_memory_test import InMemoryTest


class SessionData(BaseModel):
    user_id: str

    def __call__(self) -> str:
        return self.user_id


in_memory_backend = InMemoryBackend[UUID, SessionData]()
in_memory_test = InMemoryTest()


async def del_session(session_id: UUID = Header()) -> None:
    await in_memory_backend.delete(session_id)


async def verify_session(session_id: UUID = Header()) -> SessionData:
    id = await in_memory_backend.read(session_id)

    return id


def verify_test_session(session_id: UUID = Header()) -> SessionData:
    id = in_memory_test.read(session_id)

    return id


class SessionService:
    async def create_session(self, user_id: str, response: Response) -> UUID:
        session_id = uuid4()
        data = SessionData(user_id=user_id)

        await in_memory_backend.create(session_id, data)
        response.headers["session_id"] = str(in_memory_backend)

        return session_id

    def create_test_session(self, is_test: bool = True) -> str:
        in_memory_test.create(
            UUID("b144e64a-d40a-43d8-a2ef-4c5039b87047"), SessionData(user_id="test_id")
        )
        print(in_memory_test.read(UUID("b144e64a-d40a-43d8-a2ef-4c5039b87047")))
        return "b144e64a-d40a-43d8-a2ef-4c5039b87047"
