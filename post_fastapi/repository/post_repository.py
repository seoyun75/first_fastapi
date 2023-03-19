from typing import List

from db import get_session
from fastapi import Depends, HTTPException
from post import Post, PostUpdate
from sqlmodel import Session, select


class PostRepository:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_post(self, post: Post = Depends())->Post:
        print(self)

        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post


    def get_posts (self) -> List[Post]:
        posts = self.session.exec(select(Post)).all()
        return posts


    def get_post(self, post_id: int)->Post:
        post = self.session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post


    def update_post(self, post_id: int, post: PostUpdate):
        db_post = self.session.get(Post, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        post_data = post.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(db_post, key, value)
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post 


    def delete_post(self, post_id: int)->None :

        post = self.session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="not found")
        self.session.delete(post)
        self.session.commit()