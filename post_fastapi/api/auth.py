import logging
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from api.session import Session, backend
from domain.user import User
from fastapi import APIRouter, Depends, Header, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel
from service.user_service import UserService

router = APIRouter(prefix="/auth")


class SessionEle:
    def __init__(self) -> None:
        self.session = Session()
        self.backend = backend


@router.post("/signup")
async def signup(
    user: User,
    response: Response,
    service: UserService = Depends(),
    session_ele=Depends(SessionEle),
):
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
    # new_user = service.create_user(user)
    session_id = await session_ele.session.create_session(
        service.create_user(user).id, response, session_ele.backend
    )
    return JSONResponse(
        content=jsonable_encoder(user.id + "회원가입 성공"),
        headers=response.headers,
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/signin")
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


@router.delete("/signout")
async def delete(request: Request, session=Depends(SessionEle)):
    """
    유저 탈퇴

    Parameters :
        id : 유저id
        password : 비밀번호
    """
    print(request.get("session_id"))
    await session.session.del_session(request)
    return JSONResponse(content=None, status_code=status.HTTP_200_OK)
