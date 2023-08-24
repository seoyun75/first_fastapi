from datetime import datetime

from domain.comment import CommentBase
from domain.post import PostBase
from domain.user import UserBase
from sqlmodel import SQLModel


class SignupResponseData(UserBase):
    created_at: datetime


class SignupResponse(SQLModel):
    data: SignupResponseData


class UpdateUserResponseData(UserBase):
    created_at: datetime


class UpdateUserResponse(SQLModel):
    data: UpdateUserResponseData


class GetPostsByUserIdResponseData(PostBase):
    updated_at: datetime


class GetPostsByUserIdResponse(SQLModel):
    data: GetPostsByUserIdResponseData


class GetCommentsByUserIdResponseData(CommentBase):
    updated_at: datetime


class GetCommentsByUserIdResponse(SQLModel):
    data: GetCommentsByUserIdResponseData
