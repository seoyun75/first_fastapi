from datetime import datetime

from domain.comment import CommentBase
from domain.post import PostBase
from domain.user import UserBase
from sqlmodel import SQLModel


class SignupResponseData(UserBase):
    id: str
    created_at: datetime


class SignupResponse(SQLModel):
    data: SignupResponseData


class UpdateUserResponseData(UserBase):
    id: str
    created_at: datetime


class UpdateUserResponse(SQLModel):
    data: UpdateUserResponseData


class GetPostsByUserIdResponseData(PostBase):
    id: str
    updated_at: datetime


class GetPostsByUserIdResponse(SQLModel):
    data: GetPostsByUserIdResponseData


class GetCommentsByUserIdResponseData(CommentBase):
    id: str
    updated_at: datetime


class GetCommentsByUserIdResponse(SQLModel):
    data: GetCommentsByUserIdResponseData
