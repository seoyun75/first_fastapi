from fastapi import Depends
from sqlmodel import Session,select

from db import get_session

from domain.user import User


class UserRepository:
    
    def __init__(self, session:Session = Depends(get_session)):
        self.session = session

    def create_user(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh()

        return self.session.exec(select(User)
                                 .where(User.id == user.id, 
                                        User.password == user.password))
    
    def get_user(self, user):
        return self.session.exec(select(User)
                                 .where(User.id == user.id, 
                                        User.password == user.password))
    #session 의 컨텍스트 가 종료되는 시점 확인하기
    def get_userid(self, id):
        db_user = self.session.exec(select(User)
                                 .where(User.id == id))
        return db_user