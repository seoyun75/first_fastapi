from fastapi import APIRouter, Depends, Response, status

from api.comment.dto.request import UpdateCommentRequest
from api.comment.dto.response import (
    CreateCommentResponse,
    GetCommentsByPostIdResponse,
    UpdateCommentResponse,
)
from domain.comment import Comment
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


@router.post(
    "", response_model=CreateCommentResponse, status_code=status.HTTP_201_CREATED
)
async def create_comment(
    comment: Comment,
    session_data: SessionData = Depends(verify_session),
    service: CommentService = Depends(),
):
    """
    댓글 생성

    Parameters :
        id : 댓글id
        author_id : 작성자id
        post_id : 게시글id
        content : 댓글 내용

    Returns:
        "data" :{
                 id : 댓글id
                 author_id : 작성자id
                 post_id : 게시글id
                 content : 댓글 내용
                 created_at : 생성일자
                 updated_at : 수정일자
                }
    """
    comment.user_id = session_data.user_id

    return CreateCommentResponse(data=service.create_comment(comment))


@router.get(
    "/{post_id}",
    response_model=GetCommentsByPostIdResponse,
    status_code=status.HTTP_200_OK,
)
async def get_by_postid(post_id: int, page: int, service: CommentService = Depends()):
    """
    게시글 id에 해당하는 댓글 목록

    Parameters :
        post_id : 게시글id
        page : 댓글 페이지

    Returns:
        "data" : [
                  {
                    id : 댓글id
                    author_id : 작성자id
                    post_id : 게시글id
                    content : 댓글 내용
                    created_at : 생성일자
                    updated_at : 수정일자
                  }
                 ]
    """
    return GetCommentsByPostIdResponse(
        data=service.get_comment_by_postid(post_id, page)
    )


@router.patch(
    "",
    response_model=UpdateCommentResponse,
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_200_OK,
)
async def update_comment(
    comment: UpdateCommentRequest,
    session_data=Depends(verify_session),
    service: CommentService = Depends(),
):
    """
    댓글 내용 수정

    Parameters :
        id : 댓글id
        content : 댓글 내용

    Returns:
        "data" :{
                 id : 댓글id
                 author_id : 작성자id
                 post_id : 게시글id
                 content : 댓글 내용
                 created_at : 생성일자
                 updated_at : 수정일자
                }
    """
    comment.user_id = session_data.user_id
    return UpdateCommentResponse(data=service.update_comment(comment))


@router.delete(
    "/{id}",
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment: Comment = Depends(), service: CommentService = Depends()
):
    """
    댓글 삭제

    Parameters :
        comment_id : 댓글id
    """
    service.delete_comment(comment)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
