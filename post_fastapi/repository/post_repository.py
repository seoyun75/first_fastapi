from typing import List

from db import get_session
from fastapi import Depends
from sqlmodel import Session, select

from domain.post import Post, PostUpdate


class PostRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_post(self, post: Post = Depends()) -> Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)

        return post

    def get_posts(self) -> List[Post]:
        posts = self.session.exec(select(Post)).all()

        return posts

    def get_post(self, post_id: int) -> Post:
        post = self.session.get(Post, post_id)

        return post

    def update_post(self, post: Post) -> Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)

        return post

    def delete_post(self, post: Post) -> None:
        self.session.delete(post)
        self.session.commit()
