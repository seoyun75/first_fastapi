from typing import Optional

from datetime import datetime
from sqlmodel import SQLModel, Field

class CommentRequest(SQLModel):
    id: int
    content: str
    updated_at: datetime = Field(default_factory=datetime.today)