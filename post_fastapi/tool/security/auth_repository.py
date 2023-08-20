from db import get_session
from domain.comment import Comment
from domain.post import Post
from domain.user import User
from fastapi import Depends
from sqlmodel import Session, select


class AuthRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_target(self, object: Comment | Post | User):
        return self.session.get(type(object), object.id)

    def delete(self, id: str):
        db_comment = self.session.exec(select(Comment).where(Comment.id == id)).one()
        self.session.delete(db_comment)
        self.session.commit()
