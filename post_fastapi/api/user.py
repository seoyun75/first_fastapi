from datetime import datetime
from typing import List

from db import init_db
from domain.user import User
from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.user_service import UserService

router = APIRouter(prefix="/users")


# signup
@router.post("/signup")
async def signup(user: User, service: UserService = Depends()):
    """
    회원가입

    Parameters :
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임

    Returns:
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임
            created_at : 생성일자
    """
    new_user = service.create_user(user)

    return JSONResponse(
        content=jsonable_encoder(new_user), status_code=status.HTTP_201_CREATED
    )


# signin
@router.get("/signin")
async def signin(id: str, password: str, service: UserService = Depends()):
    """
    로그인

    Parameters :
        id : 유저id
        password : 비밀번호

    Returns:
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임
            created_at : 생성일자
    """
    user = User()
    user.id = id
    user.password = password
    signin_user = service.signin(user)
    return JSONResponse(
        content=jsonable_encoder(signin_user), status_code=status.HTTP_200_OK
    )


# update info
@router.put("/update")
async def update(user: User, service: UserService = Depends()):
    """
    유저 정보 수정

    Parameters :
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임

    Returns:
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임
            created_at : 생성일자
    """
    signin_user = service.update_user(user)
    return JSONResponse(
        content=jsonable_encoder(signin_user), status_code=status.HTTP_200_OK
    )


# #delete user
@router.delete("/delete")
async def delete(id: str, password: str, service: UserService = Depends()):
    """
    유저 탈퇴

    Parameters :
        id : 유저id
        password : 비밀번호
    """
    user = User()
    user.id = id
    user.password = password
    service.delete_user(user)
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


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
