from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.today)
    updated_at: Optional[datetime]
