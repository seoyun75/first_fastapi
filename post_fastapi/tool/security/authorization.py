from fastapi import Depends
from tool.security.auth_repository import AuthRepository


class Authorization:
    def __init__(self, auth_repository=Depends(AuthRepository)):
        self.auth_repository = auth_repository

    def verify_authority(self, object, user_id: str) -> None:
        target = self.auth_repository.get_target(object)
        if not target:
            raise Exception(args="No Content")
        elif target.user_id != user_id:
            raise Exception("No authority")
