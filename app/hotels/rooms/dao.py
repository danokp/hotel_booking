from datetime import date

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.dao.base import BaseService, GetBookedRoomsMixin
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.logger import logger


class RoomsService(GetBookedRoomsMixin, BaseService):
    model = Rooms

    @classmethod
    async def get_available_rooms_in_hotel_by_dates(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booking_days = (date_to - date_from).days
            booked_rooms = cls._get_booked_rooms(date_from, date_to)

            rooms_left = Rooms.quantity - func.coalesce(
                func.count(booked_rooms.c.room_id), 0
            )
            total_cost = Rooms.price * booking_days

            available_rooms = (
                select(
                    Rooms,
                    rooms_left.label("rooms_left"),
                    total_cost.label("total_cost"),
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .group_by(
                    Rooms.id,
                    Rooms.quantity,
                )
                .cte("available_rooms")
            )

            get_available_rooms_query_for_hotel = (
                select(available_rooms)
                .select_from(available_rooms)
                .outerjoin(Hotels, Hotels.id == available_rooms.c.hotel_id)
                .where(Hotels.id == hotel_id)
            )

            logger.debug(
                get_available_rooms_query_for_hotel.compile(
                    engine, compile_kwargs={"literal_binds": True}
                )
            )
            print(
                get_available_rooms_query_for_hotel.compile(
                    engine, compile_kwargs={"literal_binds": True}
                )
            )
            available_rooms_query_for_hotel = await session.execute(
                get_available_rooms_query_for_hotel
            )
            return available_rooms_query_for_hotel.mappings().all()

    @classmethod
    async def get_all_rooms_in_hotel_with_bookings(cls, hotel_id):
        async with async_session_maker() as session:
            rooms_with_bookings_query = (
                select(Rooms)
                .options(joinedload(Rooms.hotel))
                .options(selectinload(Rooms.bookings))
            ).filter_by(
                hotel_id=hotel_id,
            )
            rooms_with_bookings = await session.execute(rooms_with_bookings_query)
            return jsonable_encoder(rooms_with_bookings.scalars().all())
