from fastapi import Depends, HTTPException

from repository.comment_repository import CommentRepository
from domain.comment import Comment

class CommentService():
    def __init__(self, repository: CommentRepository = Depends()):
        self.repository = repository
        self.page_limit = 3

    def create_comment(self, comment: Comment):
        return self.repository.create(comment)

    def get_comment_by_postid(self, post_id: int, page:int):
        offset = (page -1) * self.page_limit
        
        return self.repository.get_by_postid(post_id, offset, self.page_limit)

    def update_comment(self, comment: Comment):
        db_comment = self.repository.get_one(comment.id)

        if db_comment == None:
            raise HTTPException(status_code=404, detail="일치하는 댓글 없음.")

        self.replace_data(db_comment, comment)

        return self.repository.update(db_comment)
    
    def delete_comment(self, id: str):
        self.repository.delete(id)

    def replace_data(self, db_comment, update_data):
        data = update_data.dict()

        for key, value in data.items():
            setattr(db_comment, key, value)