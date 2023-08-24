from api.user.dto.request import UpdateUserRequest, UserRequest
from api.user.dto.response import (
    GetCommentsByUserIdResponse,
    GetPostsByUserIdResponse,
    SignupResponse,
    UpdateUserResponse,
)
from domain.user import User
from fastapi import APIRouter, Depends, Header, Response, status
from service.user_service import UserService
from tool.security.authorization import Authorization
from tool.session import SessionData, del_session, verify_session

router = APIRouter(prefix="/users")


def verify_authority_dependency(
    user_id: str,
    session_data: SessionData = Depends(verify_session),
    auth=Depends(Authorization),
):
    return auth.verify_authority(
        User(user_id=user_id, password=""), session_data.user_id
    )


@router.post(
    "/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    user: User,
    user_service=Depends(UserService),
):
    """
    회원가입

    Parameters :
        id : 유저id
        password : 비밀번호
        nickname : 닉네임

    Returns:
        "data" :{
                  id : 유저id
                  password : 비밀번호
                  nickname : 닉네임
                  created_at : 생성일자
                }
    """
    return SignupResponse(data=user_service.create_user(user))


@router.patch(
    "/{user_id}",
    dependencies=[Depends(verify_authority_dependency)],
    response_model=UpdateUserResponse,
    status_code=status.HTTP_200_OK,
)
async def update(
    user_id: str, user: UpdateUserRequest, user_service: UserService = Depends()
):
    """
    유저 정보 수정

    Parameters :
        id : 유저id
        password : 비밀번호
        nickname : 닉네임

    Returns:
        "data" :{
                  id : 유저id
                  password : 비밀번호
                  nickname : 닉네임
                  created_at : 생성일자
                }
    """
    user.user_id = user_id
    return UpdateUserResponse(data=user_service.update_user(user))


@router.get(
    "/posts", response_model=GetPostsByUserIdResponse, status_code=status.HTTP_200_OK
)
async def get_posts(
    page: int,
    session_data: SessionData = Depends(verify_session),
    user_service: UserService = Depends(),
):
    """
    유저가 작성한 게시글 목록

    Parameters :
        id : 유저id
        page : 페이지번호

    Returns:
        "data" : [
                  {
                    id: 게시글 id
                    title: 제목
                    content: 내용
                    user_id: 작성자
                    created_at: 생성일자
                  }
                 ]
    """

    return GetPostsByUserIdResponse(
        data=user_service.get_posts(session_data.user_id, page)
    )


@router.get(
    "/comments",
    response_model=GetCommentsByUserIdResponse,
    status_code=status.HTTP_200_OK,
)
async def get_comments(
    page: int,
    session_data: SessionData = Depends(verify_session),
    user_service: UserService = Depends(),
):
    """
    유저가 작성한 댓글 목록

    Parameters :
        id : 유저id
        page : 페이지번호

    Returns:
        "data" : [
                  {
                    id: 게시글 id
                    title: 제목
                    content: 내용
                    user_id: 작성자
                  }
                 ]
    """
    return GetCommentsByUserIdResponse(
        data=user_service.get_comments(session_data.user_id, page)
    )


@router.delete(
    "/{user_id}",
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    user_id: str,
    password: str,
    user_service: UserService = Depends(),
):
    """
    유저 탈퇴

    Parameters :
        id : 유저id
        password : 비밀번호
    """
    user = UserRequest(user_id=user_id, password=password)
    user_service.delete_user(user)
    del_session()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
