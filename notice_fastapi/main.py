from datetime import datetime
from 

from fastapi import FastAPI, HTTPException

from inmemory import PostDB
from post import Post
 
app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello"}

@app.post("/post", status_code=201)
async def create_post(post : Post):
    post_list = PostDB().post_list

    post.create_date = datetime.now()

    post_list[len(post_list)+1] = post
    return post

@app.get("/get_list" status_code=200)
async def get_list():
    
    return PostDB().post_list

@app.get("/post/{id}" status_code=200)
async def post(id:int):
    post_list = PostDB().post_list
    if id not in post_list:
        raise HTTPException(status_code=404, detail="존재하지 않는 게시글입니다.")

    return post_list[id]

