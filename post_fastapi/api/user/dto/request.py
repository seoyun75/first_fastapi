from typing import Optional

from domain.user import UserBase


class UpdateUserRequest(UserBase):
    nickname: Optional[str]


class UserRequest(UserBase):
    nickname: Optional[str]
