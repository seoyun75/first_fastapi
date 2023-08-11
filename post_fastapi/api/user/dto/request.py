from datetime import datetime
from typing import Optional

from domain.user import User, UserBase


class UpdateUserRequest(UserBase):
    nickname: Optional[str]


class UserRequest(UserBase):
    nickname: Optional[str]
