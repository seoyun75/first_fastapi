from typing import List

from db import get_session
from fastapi import Depends
from sqlmodel import Session, select

from domain.post import Post


class PostRepository():

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, post: Post = Depends())->Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)

        return post

    def get_all (self)->List[Post]:
        posts = self.session.exec(select(Post)).all()

        return posts

    def get_one(self, post_id: int)->Post:
        post = self.session.get(Post, post_id)

        return post

    def update(self, post: Post)->Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)

        return post 

    def delete(self, post: Post)->None :
        self.session.delete(post)
        self.session.commit()

    def get_by_userid(self, id: str, offset: int, limit: int):
        return self.session.exec(select(Post).
                                 where(Post.user == id).order_by(Post.id).offset(offset).limit(limit)).all()