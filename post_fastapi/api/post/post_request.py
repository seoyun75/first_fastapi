from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class PostUpdate(SQLModel):
    user_id: Optional[str]
    title: Optional[str]
    content: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.today)


class CreatePost(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]
    content: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.today)
