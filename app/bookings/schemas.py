from datetime import date
from typing import Union

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseBookingSchema(BaseModel):
    """
    Schema without id and calculated fields
    """

    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class BookingSchema(BaseBookingSchema):
    id: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class BookingWithRoomInfoSchema(BookingSchema):
    image_id: int
    hotel_name: str
    room_name: str
    description: Union[str, None]
    services: list


class BookingWithRoomUserInfoSchema(BookingSchema):
    email: EmailStr
