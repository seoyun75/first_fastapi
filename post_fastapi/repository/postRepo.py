from typing import List

from sqlmodel import Session, select


from fastapi import HTTPException, Depends

from db import get_session
from post import Post, PostUpdate


class postRepository:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_post(repo, post: Post = Depends())->Post:
        repo.session.add(post)
        repo.session.commit()
        repo.session.refresh(post)
        return post


    def get_posts (self) -> List[Post]:
        posts = self.session.exec(select(Post)).all()
        return posts


    def get_post(repo, post_id: int):
        post = repo.session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post


    def update_post(repo, post_id: int, post: PostUpdate):
        db_post = repo.session.get(Post, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        post_data = post.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(db_post, key, value)
        repo.session.add(db_post)
        repo.session.commit()
        repo.session.refresh(db_post)
        return db_post # 여기서 db_post는 데이터 값이가 주소값인가


    def delete_post(repo, post_id: int):

        post = repo.session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="not found")
        repo.session.delete(post)
        repo.session.commit()
        return {"ok": True}