from pydantic import BaseModel

from app.bookings.schemas import BookingSchema
from app.hotels.schemas import HotelsSchema


class BaseRoomsSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int


class RoomsSchema(BaseRoomsSchema):
    rooms_left: int
    total_cost: int


class RoomsWithBookingsAndHotelsSchema(BaseRoomsSchema):
    bookings: list[BookingSchema]
    hotel: HotelsSchema
