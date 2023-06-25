from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRequest(SQLModel):
    id: str
    password: str
    nickname: str