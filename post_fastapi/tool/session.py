from uuid import UUID, uuid4

from fastapi import Depends, Header, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from pydantic import BaseModel


class SessionData(BaseModel):
    user_id: str

    def __call__(self) -> str:
        return self.user_id


in_memory_backend = InMemoryBackend[UUID, SessionData]()


async def del_session(session_id: UUID = Header()) -> None:
    await in_memory_backend.delete(session_id)


async def verify_session(session_id: UUID = Header()) -> SessionData:
    id = await in_memory_backend.read(session_id)

    return id


class SessionService:
    async def create_session(
        self, user_id: str, response: Response
    ) -> UUID:  #! name이 넓은 의미라 user_name 으로 변수명 변경하기 추천
        session_id = uuid4()
        data = SessionData(user_id=user_id)

        await in_memory_backend.create(session_id, data)
        response.headers["session_id"] = str(in_memory_backend)

        return session_id

    async def check(self, session_id: UUID = Depends()):
        return await in_memory_backend.read(session_id)
