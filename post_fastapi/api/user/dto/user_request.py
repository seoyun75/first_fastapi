from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRequest(SQLModel):
    id: Optional[str] = Field(default=None, primary_key=True)
    password: Optional[str]
    nickname: Optional[str]
