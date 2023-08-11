from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    id: Optional[str] = Field(index=True)
    title: str
    content: Optional[str]


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str]
    title: Optional[str]
    content: Optional[str]
    created_at: datetime = Field(default_factory=datetime.today)
    updated_at: Optional[datetime]
