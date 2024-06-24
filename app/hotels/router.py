from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelService
from app.hotels.rooms.router import router as rooms_router
from app.hotels.schemas import HotelsSchema, HotelsWithRoomsLeftSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)
router.include_router(rooms_router)


@router.get("/location/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_date(
    location: str,
    date_from: date,
    date_to: date,
) -> list[HotelsWithRoomsLeftSchema]:
    return await HotelService.get_hotels_with_available_rooms_by_dates_and_location(
        location, date_from, date_to
    )


@router.get("/{hotel_id}")
@cache(expire=60)
async def get_hotel_by_id(hotel_id: int) -> HotelsSchema:
    return await HotelService.find_one_or_none(id=hotel_id)
