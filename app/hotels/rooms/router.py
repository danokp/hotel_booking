from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.rooms.dao import RoomsService
from app.hotels.rooms.schemas import RoomsSchema, RoomsWithBookingsAndHotelsSchema

router = APIRouter(
    prefix="/{hotel_id}/rooms",
    tags=["Hotels", "Rooms"],
)


@router.get("")
@cache(expire=60)
async def get_available_rooms_in_hotel_by_date(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[RoomsSchema]:
    return await RoomsService.get_available_rooms_in_hotel_by_dates(
        hotel_id,
        date_from,
        date_to,
    )


@router.get("/bookings")
# @cache(expire=60)
async def get_all_rooms_in_hotel_with_bookings(
    hotel_id: int,
) -> list[RoomsWithBookingsAndHotelsSchema]:
    return await RoomsService.get_all_rooms_in_hotel_with_bookings(hotel_id)
