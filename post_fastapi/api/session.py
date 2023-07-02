from uuid import UUID, uuid4

from fastapi import Request, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.session_frontend import ID
from pydantic import BaseModel


class SessionData(BaseModel):
    username: str


# Uses UUID

backend = InMemoryBackend[UUID, SessionData]()


class Session:
    async def create_session(self, name: str, response: Response) -> ID:
        session = uuid4()
        data = SessionData(username=name)

        await backend.create(session, data)
        response.headers["session_id"] = str(session)
        return session

    async def check(self, session_id: str):
        return await backend.read(session_id)

    async def del_session(self, request: Request):
        print(request.headers["session_id"])
        await backend.delete(request.headers["session_id"])
        return "deleted session"
