from datetime import date

from sqlalchemy import func, select

from app.dao.base import BaseService, GetBookedRoomsMixin
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.logger import logger


class HotelService(GetBookedRoomsMixin, BaseService):
    model = Hotels

    @classmethod
    async def get_hotels_with_available_rooms_by_dates_and_location(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = cls._get_booked_rooms(date_from, date_to)

            get_hotels_with_available_query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_quantity,
                    Hotels.image_id,
                    (Hotels.rooms_quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    ),
                )
                .select_from(Hotels)
                .outerjoin(booked_rooms, booked_rooms.c.hotel_id == Hotels.id)
                .group_by(Hotels.id)
                .where(Hotels.location.like(f"%{location}%"))
            )

            logger.debug(
                get_hotels_with_available_query.compile(
                    engine, compile_kwargs={"literal_binds": True}
                )
            )

            available_rooms_query_for_hotel = await session.execute(
                get_hotels_with_available_query
            )
            return available_rooms_query_for_hotel.mappings().all()
