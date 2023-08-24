from re import match
from typing import List

from domain.comment import Comment
from domain.user import User
from fastapi import Depends, HTTPException
from repository.comment_repository import CommentRepository
from repository.post_repository import PostRepository
from repository.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repo=Depends(UserRepository),
        comment_repo=Depends(CommentRepository),
        post_repo=Depends(PostRepository),
    ):
        self.user_repo = user_repo
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.page_limit = 3

    def create_user(self, user: User) -> User:
        if self.user_repo.get_user_byid(user.user_id) != None:
            raise HTTPException(status_code=400, detail="중복된 아이디입니다.")

        if not self.check_password(user.password):
            raise HTTPException(status_code=400, detail="사용할 수 없는 비밀번호 입니다.")
        return self.user_repo.create_user(user)

    def signin(self, user: User) -> User:
        signin_user = self.user_repo.get_user(user)

        if signin_user == None:
            raise HTTPException(status_code=404, detail="일치하는 정보가 없습니다.")

        return signin_user

    def update_user(self, user: User) -> User:
        db_user = self.user_repo.get_user_byid(user.user_id)

        if db_user == None:
            raise HTTPException(status_code=404, detail="id 와 일치하는 유저정보 없음.")

        user_typedict = user.dict(exclude_unset=True)

        for key, value in user_typedict.items():
            setattr(db_user, key, value)

        return self.user_repo.update_user(db_user)

    def delete_user(self, user: User) -> None:
        self.user_repo.delete_user(user)

    def get_posts(self, id: str, page) -> List:
        offset = (page - 1) * self.page_limit

        return self.post_repo.get_by_userid(id, offset, self.page_limit)

    def get_comments(self, id: str, page) -> List[Comment]:
        offset = (page - 1) * self.page_limit
        return self.comment_repo.get_by_userid(id, offset, self.page_limit)

    def check_password(self, password):
        pattern = r"^(?=.*[A-Z])(?=.{8,})"
        return match(pattern, password)
