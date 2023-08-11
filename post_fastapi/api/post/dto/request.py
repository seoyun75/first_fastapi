from datetime import datetime
from typing import Optional

from domain.post import PostBase
from sqlmodel import Field, SQLModel


class UpdatePostRequst(PostBase):
    user_id: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.today)


class CreatePostRequest(PostBase):
    user_id: Optional[str]
    create_at: datetime = Field(default_factory=datetime.today)
