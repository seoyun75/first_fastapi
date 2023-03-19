from datetime import datetime
from typing import List
from db import init_db
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from post import Post, PostCreate, PostUpdate
from repository.post_repository import PostRepository

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root(post_repo: PostRepository = Depends()):
    print(post_repo.session)
    return Response(content="ok",status_code=status.HTTP_200_OK)

@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_posts(post_repo : PostRepository=Depends(PostRepository)):
    """
    게시글id와 게시글 전체를 반환합니다.

    Returns:
        dict[int, Post]: 게시글 리스트
    """
    posts = post_repo.get_posts()
    
    return JSONResponse(content=jsonable_encoder(posts), status_code=status.HTTP_200_OK)

@app.get("/posts/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(id: int, post_repo : PostRepository=Depends()):
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
    post = post_repo.get_post(id)
    post_json = jsonable_encoder(post)
    
    return JSONResponse(content=post_json, status_code=status.HTTP_200_OK)

@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post : Post, post_repo: PostRepository = Depends()):
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
    post.create_date = datetime.now()


    # json_data = jsonable_encoder(post_db)

    return post_repo.create_post(post)

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: PostUpdate, post_repo: PostRepository = Depends()):
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
    new_post = post_repo.update_post(id, post)
    print(new_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, post_repo : PostRepository=Depends()):
    post_repo.delete_post(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
