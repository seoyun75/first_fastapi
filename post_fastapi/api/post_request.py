from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class PostUpdate(SQLModel):
    user: Optional[str]
    title: Optional[str]
    content: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.today)
