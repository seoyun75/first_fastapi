from db import get_session
from domain.post import Post
from fastapi import Depends
from sqlmodel import Session


class TestRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_post(self, post: Post):
        item = Post(**post)
        self.session.add(item)
        self.session.commit()
