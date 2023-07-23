from api import auth, comment, post, user
from click import UUID
from db import init_db
from fastapi import Depends, FastAPI

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(post.router, tags=["posts"])
app.include_router(comment.router, tags=["comments"])

# @app.exception_handler(RequestValidationError)
