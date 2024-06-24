from typing import Optional

from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"


class IncorrectFormatTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect format token"


class NoUserException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Room is not available to be booked"


class BookingCannotBeDeletedException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "The booking cannot be deleted"


class BookingCannotBeFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "No booking with this id available"
