import re

from fastapi import HTTPException, Depends

from domain.user import User
from repository.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository

    def create_user(self, user: User):
        #idaready
        if self.repository.get_userid(user.id) != None:
            raise print("중복 아이디 오류발생")
        #passwordwrongpattern
        if check_password(user.password):
            raise HTTPException #not password format 오류 발생시키기
        return self.repository.create_user(user)

    # def signin()
    def signin(self, user: User):
        signin_user = self.repository.get_user(user)

        if signin_user == None:
            raise HTTPException #일치하는 정보가 없습니다.
        
        return signin_user

    # def update_user()


    # def delete_user()

    
def check_password(password):
    pattern = r'^(?=.*[A-Z])(?=.{8,})'
    return re.match(pattern, password)