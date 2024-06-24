from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectFormatTokenException,
    NoUserException,
    TokenAbsentException,
)
from app.users.consts import BOOKING_ACCESS_TOKEN_NAME
from app.users.dao import UsersService


def get_token(request: Request):
    token = request.cookies.get(BOOKING_ACCESS_TOKEN_NAME)
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectFormatTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserException

    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise NoUserException
    return user
