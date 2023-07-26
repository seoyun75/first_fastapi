from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CommentRequest(SQLModel):
    id: int
    author_id: str
    post_id: int
    content: str


class CommentUpdate(SQLModel):
    id: int
    content: str
    updated_at: datetime = Field(default_factory=datetime.today)
