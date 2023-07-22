from api.user_dto import UserRequest
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.user_service import UserService
from tool.session import SessionService, del_session, verify_session

router = APIRouter(prefix="/auth")


@router.post("/signin", status_code=status.HTTP_201_CREATED)
async def signin(
    user: UserRequest,
    response: Response,
    service=Depends(UserService),
    session=Depends(SessionService),
):
    """
    로그인

    Parameters :
        id : 유저id
        password : 비밀번호

    Returns:
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임
            created_at : 생성일자
    """
    session_data = await session.create_session(service.signin(user).id, response)
    return JSONResponse(
        content=jsonable_encoder(session_data), status_code=status.HTTP_201_CREATED
    )


@router.get("/userid", status_code=status.HTTP_200_OK)
async def check_userid(request: Request, user_id: str = Depends(verify_session)):
    return JSONResponse(
        content=jsonable_encoder(user_id), status_code=status.HTTP_200_OK
    )


@router.post(
    "/signout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(del_session)],
)
async def signout():
    """
    유저 탈퇴

    Parameters :
        id : 유저id
        password : 비밀번호
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)
