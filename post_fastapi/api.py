from datetime import datetime
from typing import List
from db import init_db
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from domain.post import Post, PostUpdate
from service.post_service import PostService

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/healthcheck")
async def root(post_service: PostService = Depends()):
    print(post_service)
    return Response(content="ok", status_code=status.HTTP_200_OK)


@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_posts(post_service: PostService = Depends()):
    """
    게시글id와 게시글 전체를 반환합니다.

    Returns:
        dict[int, Post]: 게시글 리스트
    """
    posts = post_service.get_posts()

    return JSONResponse(content=jsonable_encoder(posts), status_code=status.HTTP_200_OK)


@app.get("/posts/{id}", response_model=Post, status_code=status.HTTP_200_OK)
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


    """
    post = post_service.get_post(id)
    post_json = jsonable_encoder(post)

    return JSONResponse(content=post_json, status_code=status.HTTP_200_OK)


@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, post_service: PostService = Depends()):
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
    post = post_service.create_post(post)

    return JSONResponse(
        content=jsonable_encoder(post), status_code=status.HTTP_201_CREATED
    )


@app.patch("/posts/{id}", status_code=status.HTTP_200_OK)
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
    post = post_service.update_post(id, post)

    return JSONResponse(content=jsonable_encoder(post), status_code=status.HTTP_200_OK)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, post_service: PostService = Depends()):
    post_service.delete_post(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
