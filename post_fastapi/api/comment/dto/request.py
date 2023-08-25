from datetime import datetime
from typing import Optional

from domain.comment import CommentBase
from sqlmodel import Field


class CreateCommentRequest(CommentBase):
    user_id: str


class UpdateCommentRequest(CommentBase):
    user_id: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.today)
