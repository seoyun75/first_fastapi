from datetime import datetime
from typing import Any, List, Optional

from domain.post import PostBase
from pydantic import BaseModel


class GetPostModel(PostBase):
    user_id: str


class GetPostsResponse(BaseModel):
    data: List[GetPostModel]


class GetPostResponse(BaseModel):
    data: GetPostModel


class CreatePostModel(PostBase):
    user_id: Optional[str]
    created_at: datetime


class CreatePostResponse(BaseModel):
    data: CreatePostModel


class UpdatePostModel(PostBase):
    user_id: str
    created_at: datetime
    updated_at: datetime


class UpdatePostResponse(BaseModel):
    data: UpdatePostModel
