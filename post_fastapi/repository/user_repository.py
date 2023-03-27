from fastapi import Depends
from sqlmodel import Session,select

from db import get_session

from domain.user import User
from domain.post import Post


class UserRepository:
    
    def __init__(self, session:Session = Depends(get_session)):
        self.session = session

    def create_user(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return self.get_user(user)
    
    def get_user(self, user):
        return self.session.exec(select(User)
                                 .where(User.id == user.id, 
                                        User.password == user.password)).first()
    #session 의 컨텍스트 가 종료되는 시점 확인하기
    def get_user_byid(self, id):
        db_user = self.session.exec(select(User)
                                 .where(User.id == id)).first()
        return db_user
    
    def update_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return self.get_user(user)

    def delete_user(self, user: User):
        self.session.delete(self.get_user(user))
        self.session.commit()