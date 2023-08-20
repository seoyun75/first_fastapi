from sqlite3 import IntegrityError
from typing import List

from domain.post import Post
from fastapi import Depends
from repository.post_repository import PostRepository


class PostService:
    def __init__(self, post_repo: PostRepository = Depends()):
        self.post_repo = post_repo

    def get_posts(self) -> List[Post]:
        return self.post_repo.get_all()

    def get_post(self, post_id: int) -> Post:
        return self.post_repo.get_one(post_id)

    def create_post(self, post: Post) -> Post:
        if self.get_post(post.id):
            raise IntegrityError()

        return self.post_repo.create(post)

    def update_post(self, post_id: int, update_data: Post) -> Post:
        db_post = self.post_repo.get_one(post_id)

        return self.post_repo.update(self.replace_postdata(update_data, db_post))

    def delete_post(self, post_id: int) -> None:
        post = self.get_post(post_id)
        self.post_repo.delete(post)

    def replace_postdata(self, update_data: Post, db_post: Post) -> Post:
        data = update_data.dict(exclude_none=True)

        for key, value in data.items():
            setattr(db_post, key, value)

        return db_post
