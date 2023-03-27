from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from api import user, post, comment
from db import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router, tags=["users"])
app.include_router(post.router, tags=["posts"])
app.include_router(comment.router, tags=["comments"])

# @app.exception_handler(RequestValidationError)