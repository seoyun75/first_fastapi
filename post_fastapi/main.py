import uvicorn
from api import auth
from api.comment import comment_endpoint
from api.post import post_endpoint
from api.user import user_endpoint
from db import init_db
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(user_endpoint.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(post_endpoint.router, tags=["posts"])
app.include_router(comment_endpoint.router, tags=["comments"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
