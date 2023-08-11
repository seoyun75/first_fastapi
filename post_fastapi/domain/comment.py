from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CommentBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    post_id: Optional[int]
    content: Optional[str]


class Comment(CommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str]
    post_id: Optional[int]
    content: Optional[str]
    created_at: datetime = Field(default_factory=datetime.today)
    updated_at: Optional[datetime]
