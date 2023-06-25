from datetime import datetime
from typing import List

from api.post_request import PostUpdate
from domain.post import Post
from fastapi import Depends
from repository.post_repository import PostRepository


class PostService:
    def __init__(self, post_repo: PostRepository = Depends()):
        self.post_repo = post_repo

    def get_posts(self) -> List[Post]:
        return self.post_repo.get_all()

    def get_post(self, id: int) -> Post:
        return self.post_repo.get_one(id)

    def create_post(self, post: Post) -> Post:
        return self.post_repo.create(post)

    def update_post(self, id: int, update_data: PostUpdate) -> Post:
        update_data.updated_at = datetime.today()

        db_post = self.post_repo.get_one(id)

        return self.post_repo.update(self.replace_postdata(update_data, db_post))

    def delete_post(self, id: int):
        post = self.get_post(id)
        self.post_repo.delete(post)

    def replace_postdata(self, updata_data: Post, db_post: Post):
        data = updata_data.dict(exclude_unset=True)

        for key, value in data.items():
            setattr(db_post, key, value)

        return db_post
