from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.consts import BOOKING_ACCESS_TOKEN_NAME
from app.users.dao import UsersService
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import GetUserSchema, UserAuthSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register")
async def register_user(user_data: UserAuthSchema):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(BOOKING_ACCESS_TOKEN_NAME, access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(BOOKING_ACCESS_TOKEN_NAME)


@router.get("/me")
async def read_current_user(
    current_user: Users = Depends(get_current_user),
) -> GetUserSchema:
    return current_user
