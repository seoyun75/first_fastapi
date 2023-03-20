from datetime import datetime
from typing import List

from fastapi import Depends
from domain.post import Post, PostUpdate
from repository.post_repository import PostRepository


class PostService:
    def __init__(self, post_repo: PostRepository = Depends()):
        self.post_repo = post_repo

    def get_posts(self) -> List[Post]:
        return self.post_repo.get_posts()

    def get_post(self, id: int) -> Post:
        return self.post_repo.get_post(id)

    def create_post(self, post: Post) -> Post:
        return self.post_repo.create_post(post)

    def update_post(self, id: int, post: PostUpdate) -> Post:
        db_post = self.post_repo.get_post(id)
        post_data = post.dict(exclude_unset=True)

        for key, value in post_data.items():
            setattr(db_post, key, value)

        return self.post_repo.update_post(db_post)

    def delete_post(self, id: int):
        post = self.get_post(id)
        self.post_repo.delete_post(post)
