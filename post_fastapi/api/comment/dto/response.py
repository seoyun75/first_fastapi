from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel

from domain.comment import CommentBase


class CreateCommentResponseData(CommentBase):
    user_id: Optional[str]
    created_at: Optional[datetime]


class CreateCommentResponse(SQLModel):
    data: CreateCommentResponseData


class GetCommentsByPostIdResponseData(CommentBase):
    user_id: Optional[str]
    created_at: datetime


class GetCommentsByPostIdResponse(SQLModel):
    data: List[GetCommentsByPostIdResponseData]


class UpdateCommentResponseData(CommentBase):
    user_id: Optional[str]
    updated_at: datetime


class UpdateCommentResponse(SQLModel):
    data: UpdateCommentResponseData
