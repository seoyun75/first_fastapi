from datetime import datetime
from typing import List

from api.post.post_request import PostUpdate
from domain.post import Post
from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.post_service import PostService
from tool.session import verify_session

router = APIRouter(prefix="/posts")


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[Post]
)  # 파라미터의 순서 일관된게 맞추기
async def get_posts(post_service: PostService = Depends()):
    """
    게시글id와 게시글 전체를 반환합니다.

    Returns:
        dict[int, Post]: 게시글 리스트
    """
    posts = post_service.get_posts()

    return JSONResponse(content=jsonable_encoder(posts), status_code=status.HTTP_200_OK)


@router.get("/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(id: int, post_service: PostService = Depends()):
    """
        id 값에 해당하는 게시물 반환합니다.

        Parameters :
            id : 게시물의 id

        Return :
            Post :
                user: 작성자
                title: 제목
                content : 글 내용
                create_date : 생성 시간
    #!의미 없는 개행 삭제

    """
    post = post_service.get_post(id)
    post_json = jsonable_encoder(post)

    return JSONResponse(content=post_json, status_code=status.HTTP_200_OK)


@router.post("", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create(
    post: Post,
    user: str = Depends(verify_session),  #! user, user_id 이름 맞추기
    post_service: PostService = Depends(),
):
    """
    새로운 게시물을 생성합니다.

    Parameter :
        post :
            user: 작성자
            title: 제목
            content : 글 내용

    Return :
        Post :
            user: 작성자
            title: 제목
            content : 글 내용
            create_date : 생성 시간


    """
    post.user = user.username
    post = post_service.create_post(post)

    return JSONResponse(
        content=jsonable_encoder(post), status_code=status.HTTP_201_CREATED
    )


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post: PostUpdate, post_service: PostService = Depends()):
    """
    기존 게시물의 내용을 변경합니다.

    Param :
        id : 게시글 id
        post :
            user: 작성자
            title: 제목
            content : 글 내용
    Return :
        Post :
            user: 작성자
            title: 제목
            content : 글 내용
            create_date : 생성 시간


    """
    post = post_service.update_post(id, post)  # 해당 유저만 수정가능하게 수정()

    return JSONResponse(content=jsonable_encoder(post), status_code=status.HTTP_200_OK)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, post_service: PostService = Depends()):
    post_service.delete_post(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)