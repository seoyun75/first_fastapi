from datetime import datetime

from fastapi import FastAPI, Response, HTTPException, status

from post import Post
from inmemory import PostDB
 
app = FastAPI()

@app.get("/")
async def root():
    return Response(content="ok",status_code=status.HTTP_200_OK)

@app.get("/post")
async def get_postlist():
    post_list = PostDB().post_list
    """
    게시글id와 게시글 전체를 반환합니다.

    Returns:
        dict[int, Post]: 게시글 리스트
    """
    return Response(content=post_list, status_code=status.HTTP_200_OK)

@app.get("/post/{id}")
async def get_post(id:int):
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
    post_list = PostDB().post_list
    if id not in post_list:
        raise HTTPException(status_code=404, detail="존재하지 않는 게시글입니다.")

    return Response(content=post_list[id], status_code=status.HTTP_200_OK)

@app.post("/post", status_code=201)
async def create_post(post : Post):
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

    post_list = PostDB().post_list

    post.create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    post_list[len(post_list)+1] = post
    return Response(content=post, status_code=status.HTTP_201_CREATED)

@app.put("/update/{id}")
async def update_post(id:int, post : Post):
    """
    기존 게시물의 내용을 변경합니다.
    
    Param : 
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
    post_list = PostDB().post_list

    if id not in post_list:
        raise HTTPException(status_code=404, detail="존재하지 않는 게시글입니다.")
    else:
        target_post = post_list[id]

    if target_post.user != post.user:
        raise HTTPException(status_code = 403, detail="수정 불가능한 게시글 입니다.")

    target_post.title, target_post.content = post.title, post.content
    post_list[id] = target_post

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/post/{id}")
async def delete_post(id:int):
    post_list = PostDB().post_list
    post_list.pop(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)