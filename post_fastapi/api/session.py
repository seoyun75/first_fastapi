from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, Request, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.session_frontend import ID
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel


class SessionData(BaseModel):
    username: str


class SessionService:
    async def create_session(
        self, name: str, response: Response, session: InMemoryBackend = Depends()
    ) -> UUID:
        session_id = uuid4()
        data = SessionData(username=name)

        await session.create(session_id, data)
        response.headers["session_id"] = str(session)
        return session_id

    async def check(self, session_id: ID, session: InMemoryBackend = Depends()):
        print(session_id, session.data)
        return await session.read(session_id)

    def del_session(self, request: Request, session: InMemoryBackend):
        session.delete(request.headers["session_id"])
        return "deleted session"
