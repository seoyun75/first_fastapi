from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str
    title: str
    content: str
    create_date: datetime = Field(default_factory=datetime.today)


class PostUpdate(SQLModel):
    user: Optional[str]
    title: Optional[str]
    content: Optional[str]


class PostCreate(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str
    title: str
    content: str
