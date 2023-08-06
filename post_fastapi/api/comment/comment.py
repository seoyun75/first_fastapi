from datetime import datetime
from typing import List

from api.comment.dto.comment_request import CommentUpdate
from domain.comment import Comment
from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.comment_service import CommentService
from tool.security.authorization import Authorization
from tool.session import SessionData, verify_session

router = APIRouter(prefix="/comments")


def verify_authority_dependency(
    comment: Comment,
    session_data: SessionData = Depends(verify_session),
    auth=Depends(Authorization),
):
    return auth.verify_authority(Comment(id=comment.id), session_data.user_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: Comment,
    session_data: SessionData = Depends(verify_session),
    service: CommentService = Depends(),
):
    """
    댓글 생성

    Parameters :
        Comment :
            id : 댓글id
            author_id : 작성자id
            post_id : 게시글id
            content : 댓글 내용

    Returns:
        Comment :
            id : 댓글id
            author_id : 작성자id
            post_id : 게시글id
            content : 댓글 내용
            created_at : 생성일자
            updated_at : 수정일자
    """
    comment.user_id = session_data.user_id
    new_comment = service.create_comment(comment)

    return JSONResponse(
        content=jsonable_encoder(new_comment), status_code=status.HTTP_201_CREATED
    )


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def get_by_postid(post_id: int, page: int, service: CommentService = Depends()):
    """
    게시글 id에 해당하는 댓글 목록

    Parameters :
        Comment :
            post_id : 게시글id
            page : 댓글 페이지

    Returns:
        List[Comment]
    """
    comments = service.get_comment_by_postid(post_id, page)

    return JSONResponse(
        content=jsonable_encoder(comments), status_code=status.HTTP_200_OK
    )


@router.patch(
    "",
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_200_OK,
)
async def update_comment(comment: CommentUpdate, service: CommentService = Depends()):
    """
    댓글 내용 수정

    Parameters :
        Comment :
            id : 댓글id
            content : 댓글 내용

    Returns:
        Comment :
            id : 댓글id
            author_id : 작성자id
            post_id : 게시글id
            content : 댓글 내용
            created_at : 생성일자
            updated_at : 수정일자
    """
    update_comment = service.update_comment(comment)

    return JSONResponse(
        content=jsonable_encoder(update_comment), status_code=status.HTTP_200_OK
    )


@router.delete(
    "",
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(comment_id: str, service: CommentService = Depends()):
    """
    댓글 삭제

    Parameters :
        id : 댓글id
    """
    service.delete_comment(comment_id)

    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
