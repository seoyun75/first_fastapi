from typing import Dict
from uuid import UUID

from fastapi_sessions.backends.session_backend import BackendError
from pydantic import BaseModel


class InMemoryTest:
    def __init__(self) -> None:
        """Initialize a new in-memory database."""
        self.data: Dict[UUID, BaseModel] = {}

    def create(self, session_id: UUID, data: BaseModel):
        """Create a new session entry."""
        if self.data.get(session_id):
            raise BackendError("create can't overwrite an existing session")

        self.data[session_id] = data.copy(deep=True)

    def read(self, session_id: UUID):
        """Read an existing session data."""
        data = self.data.get(session_id)
        if not data:
            return

        return data.copy(deep=True)

    def update(self, session_id: UUID, data: BaseModel) -> None:
        """Update an existing session."""
        if self.data.get(session_id):
            self.data[session_id] = data
        else:
            raise BackendError("session does not exist, cannot update")

    def delete(self, session_id: UUID) -> None:
        """D"""
        del self.data[session_id]
