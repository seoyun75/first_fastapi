from datetime import datetime
from typing import List

from domain.user import User
from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.user_service import UserService

router = APIRouter(prefix="/users")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
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


@router.put(
    "/user", status_code=status.HTTP_200_OK
)  #! put 에 안쓰고 users/{user_id} - user_id 를 통해
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


@router.get("/posts", status_code=status.HTTP_200_OK)  # 계층 구조에 따라서 작성 posts?user_id
# 식별자를 path 에 넣고 property는 쿼리 파라미터
async def get_posts(
    id: str, page: int, service: UserService = Depends()
):  # id 라고 안하고 명확하게 작정
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


@router.get("/comments", status_code=status.HTTP_200_OK)
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


@router.delete(
    "/user", status_code=status.HTTP_204_NO_CONTENT
)  # ! DELETE users/ + token
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
