from datetime import datetime
from typing import List

from db import init_db
from domain.user import User
from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.user_service import UserService

router = APIRouter(prefix="/users")


@router.get("/posts")
async def get_posts(id: str, page: int, service: UserService = Depends()):
    """
    유저가 작성한 게시글 목록

    Parameters :
        id : 유저id
        page : 페이지번호

    Returns:
        List[Post]
    """
    user = User()
    user.id = id

    posts = service.get_posts(id, page)
    return JSONResponse(content=jsonable_encoder(posts), status_code=status.HTTP_200_OK)


@router.get("/comments")
async def get_comments(id: str, page: int, service: UserService = Depends()):
    """
    유저가 작성한 댓글 목록

    Parameters :
        id : 유저id
        page : 페이지번호

    Returns:
        List[Comment]
    """
    comments = service.get_comments(id, page)
    return JSONResponse(
        content=jsonable_encoder(comments), status_code=status.HTTP_200_OK
    )
