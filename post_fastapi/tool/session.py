from uuid import UUID, uuid4

from fastapi import Depends, Header, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from pydantic import BaseModel


class SessionData(BaseModel):
    username: str


in_memory_backend = InMemoryBackend[UUID, SessionData]()


async def del_session(session_id: UUID = Header()) -> None:
    await in_memory_backend.delete(session_id)


async def verify_session(session_id: UUID = Header()) -> str:
    return await in_memory_backend.read(session_id)


class SessionService:
    async def create_session(self, name: str, response: Response) -> UUID:
        session_id = uuid4()
        data = SessionData(username=name)

        await in_memory_backend.create(session_id, data)
        response.headers["session_id"] = str(in_memory_backend)
        return session_id

    async def check(self, session_id: UUID = Depends()):
        return await in_memory_backend.read(session_id)
