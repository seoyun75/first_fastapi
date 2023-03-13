from datetime import datetime

from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from post import Post, PostUpdate, PostCreate
from repository.postRepo import postRepository, get_posts
from db import init_db
 
app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root(post_repo: postRepository = Depends()):
    print(post_repo.session)
    return Response(content="ok",status_code=status.HTTP_200_OK)

@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_postlist(repo : postRepository=Depends()):
    post_list = postRepository.get_posts(repo)
    """
    게시글id와 게시글 전체를 반환합니다.

    Returns:
        dict[int, Post]: 게시글 리스트
    """
    return post_list

@app.get("/posts/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(id: int, repo : postRepository=Depends()):
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
    post_list = postRepository.get_posts(repo, id)

    return Response(content=post_list[id], status_code=status.HTTP_200_OK)

@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(repo : postRepository=Depends(), post : Post=Depends()):
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
    print("start------------")
    post.create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("db conect---------")
    post_db = create_post(post)

    # json_data = jsonable_encoder(post_db)
    print("end")
    return post_db

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id:int,repo : postRepository=Depends(), post : PostUpdate = Depends()):
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
    post_db = postRepository.update_post(repo, id, post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, repo : postRepository=Depends()):
    post_list = PostDB().post_list
    post_list.pop(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
