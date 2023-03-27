
from sqlmodel import Session, select
from fastapi import Depends

from domain.comment import Comment
from db import get_session

class CommentRepository():
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, comment: Comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

        return self.get_one(comment.id)
    
    def get_by_userid(self, id:str, page:int, limit:int):
        return self.session.exec(select(Comment).where(Comment.author_id == id).offset(page).limit(limit)).all()

    def get_by_postid(self, id:str, page:int, limit:int):
        return self.session.exec(select(Comment).where(Comment.post_id == id).offset(page).limit(limit)).all()

    def delete(self, id:str):
        db_comment = self.session.exec(select(Comment).where(Comment.id == id)).one()
        self.session.delete(db_comment)

        self.session.commit()

    def update(self, comment: Comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

        return self.get_one(comment.id)

    def get_one(self, id):
        return self.session.exec(select(Comment).where(Comment.id == id)).first()