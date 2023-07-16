from typing import Annotated
from uuid import UUID

from api.session import SessionData, SessionService
from api.user_dto import UserRequest
from domain.user import User
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from service.user_service import UserService

router = APIRouter(prefix="/auth")
inmemory = InMemoryBackend[UUID, SessionData]()


@router.post("/signup", status_code=200)
async def signup(
    user: User,
    service=Depends(UserService),
):
    """

    ver 체크(x)-> 회원가입 프로세스 -> 세션저장 -> 세션 id 반환
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
        content=jsonable_encoder("회원가입 성공"), status_code=status.HTTP_201_CREATED
    )


@router.post("/signin", status_code=200)
async def signin(
    user: UserRequest,
    response: Response,
    service=Depends(UserService),
    session=Depends(SessionService),
):
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
    signin_user = service.signin(user)
    session_data = await session.create_session(signin_user.id, response, inmemory)
    return JSONResponse(
        content=jsonable_encoder(session_data), status_code=status.HTTP_200_OK
    )


@router.delete("/signout", status_code=206)
async def delete(request: Request, session=Depends(SessionService)):
    """
    유저 탈퇴

    Parameters :
        id : 유저id
        password : 비밀번호
    """
    session.del_session(request, inmemory)
    return JSONResponse(content=None, status_code=status.HTTP_206_PARTIAL_CONTENT)


@router.get("/userid")
async def delete(request: Request, session=Depends(SessionService)):
    user_data = await session.check(request.headers["session_id"], inmemory)

    return JSONResponse(
        content=jsonable_encoder(user_data), status_code=status.HTTP_200_OK
    )


@router.delete("/user", status_code=204)
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
