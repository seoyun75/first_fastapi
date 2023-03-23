from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db import init_db
from post_fastapi.domain.user import User
from post_fastapi.service.user_service import UserService

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/user")
async def root():
    return Response(content="ok", status_code=status.HTTP_200_OK)

#signup
@app.post("/user/signup")
async def signup(user:User, service:UserService=Depends()):
    new_user = service.create_user(user)

    return JSONResponse(content=jsonable_encoder(new_user), status_code=status.HTTP_201_CREATED)
#signin
@app.get("/user/signin")
async def signin(user:User, service:UserService=Depends()):
    signin_user = service.signin(user)

    return JSONResponse(content=jsonable_encoder(signin_user), status_code=status.HTTP_200_OK)
    
#update info
# @app.patch("/user/update")
# #delete user
# @app.delete("/user/delete")