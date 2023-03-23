
#login
#- 유저 아이디 (Id)
# - 유저 비밀번호 (Password)
#     - 길이는 최소 8자 이상이여야 합니다.
#     - 대문자 1개 이상이 꼭 들어가야 합니다.
# - 유저 닉네임 (Nickname)
# - 유저 생성 날짜 (Created At)
#

from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel

class User(SQLModel, table=True, extend_existing=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    password: str
    nickname: str
    created_at: datetime = Field(default_factory=datetime.today)
