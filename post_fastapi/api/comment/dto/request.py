from datetime import datetime
from typing import Optional

from sqlmodel import Field

from domain.comment import CommentBase


class CreateCommentRequest(CommentBase):
    user_id: str


class UpdateCommentRequest(CommentBase):
    user_id: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.today)
