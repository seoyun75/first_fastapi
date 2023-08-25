from api.post.dto.request import UpdatePostRequst
from api.post.dto.response import (
    CreatePostResponse,
    GetPostResponse,
    GetPostsResponse,
    UpdatePostResponse,
)
from domain.post import Post
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import PlainTextResponse
from service.post_service import PostService
from tool.security.authorization import Authorization
from tool.session import SessionData, verify_session

router = APIRouter(prefix="/posts")


def verify_authority_dependency(
    post_id: str,
    session_data: SessionData = Depends(verify_session),
    auth=Depends(Authorization),
):
    return auth.verify_authority(Post(id=post_id), session_data.user_id)


@router.get("", response_model=GetPostsResponse, status_code=status.HTTP_200_OK)
async def get_posts(post_service: PostService = Depends()):
    """
    게시글의 id, 제목, 내용, 작성자를 list로 반환합니다.

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

    return GetPostsResponse(data=post_service.get_posts())


@router.get(
    "/{post_id}", response_model=GetPostResponse, status_code=status.HTTP_200_OK
)
async def get_post(post_id: int, post_service: PostService = Depends()):
    """
    id 값에 해당하는 게시물 반환합니다.

    Parameters :
        id : 게시물의 id

    Return :
        "data" : {
                    id: 게시글 id
                    title: 제목
                    content: 내용
                    user_id: 작성자
                 }
    """
    return GetPostResponse(data=post_service.get_post(post_id))


@router.post("", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create(
    post: Post,
    session_data: SessionData = Depends(verify_session),
    post_service: PostService = Depends(),
):
    """
    새로운 게시물을 생성합니다.

    Parameter :
        post :
            title: 제목
            content : 글 내용

    Return :
        "data" : {
                    id: 게시글 id
                    title: 제목
                    content: 내용
                    user_id: 작성자
                 }
    """
    post.user_id = session_data.user_id

    return CreatePostResponse(data=post_service.create_post(post))


@router.patch(
    "/{post_id}",
    response_model=UpdatePostResponse,
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: int, post: UpdatePostRequst, post_service: PostService = Depends()
):
    """
    기존 게시물의 내용을 변경합니다.

    Param :
        id : 게시글 id
        post :
            user: 작성자
            title: 제목
            content : 글 내용

    Return :
        "data" : {
                    id: 게시글 id
                    title: 제목
                    content: 내용
                    user_id: 작성자
                 }
    """
    return UpdatePostResponse(data=post_service.update_post(post_id, post))


@router.delete(
    "/{post_id}",
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(post_id: int, post_service: PostService = Depends()):
    post_service.delete_post(post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
