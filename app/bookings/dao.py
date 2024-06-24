from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseService
from app.database import async_session_maker, async_session_maker_nullpool, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.logger import logger
from app.users.models import Users


class BookingService(BaseService):
    model = Bookings
    session_maker = async_session_maker

    @staticmethod
    def _get_bookings_by_filter_query(**filter_by):
        return (
            select(
                Bookings.__table__.columns,
                Rooms.image_id,
                Rooms.name.label("room_name"),
                Rooms.description,
                Rooms.services,
                Hotels.name.label("hotel_name"),
            )
            .filter_by(**filter_by)
            .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
            .join(Hotels, Hotels.id == Rooms.hotel_id, isouter=True)
        )

    @classmethod
    async def get_all_bookings_for_user_by_filter(cls, user_id: int, **filter_by):
        try:
            async with cls.session_maker() as session:
                get_all_bookings_query = cls._get_bookings_by_filter_query(
                    user_id=user_id, **filter_by
                )
                all_bookings = await session.execute(get_all_bookings_query)
                return all_bookings.mappings().all()
        except SQLAlchemyError:
            logger.error(
                msg="Database Error",
                extra={"user_id": user_id, "filter_by": filter_by},
                exc_info=True,
            )

    @classmethod
    async def get_all_bookings_with_user_info_by_filter(cls, **filter_by):
        async with cls.session_maker() as session:
            get_all_bookings_query = (
                select(
                    Bookings.__table__.columns,
                    Rooms.image_id,
                    Rooms.name.label("room_name"),
                    Rooms.description,
                    Rooms.services,
                    Hotels.name.label("hotel_name"),
                    Users.email,
                )
                .filter_by(**filter_by)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .join(Hotels, Hotels.id == Rooms.hotel_id, isouter=True)
                .join(Users, Bookings.user_id == Users.id, isouter=True)
            )
            all_bookings = await session.execute(get_all_bookings_query)
            return all_bookings.mappings().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        async with cls.session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left_query = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )
            logger.debug(
                get_rooms_left_query.compile(
                    engine, compile_kwargs={"literal_binds": True}
                )
            )
            rooms_left = await session.execute(get_rooms_left_query)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price_query = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price_query)
                price: int = price.scalar()
                add_booking_query = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings.id)
                )

                new_booking = await session.execute(add_booking_query)
                await session.commit()
                return new_booking.scalar()

    @classmethod
    async def delete(cls, booking_id: int, user_id: int):
        async with cls.session_maker() as session:
            delete_booking_query = (
                delete(Bookings)
                .filter_by(
                    user_id=user_id,
                    id=booking_id,
                )
                .returning(Bookings)
            )
            delete_booking = await session.execute(delete_booking_query)
            await session.commit()
            return delete_booking.scalar()

    @classmethod
    async def get(cls, booking_id: int, user_id: int):
        async with cls.session_maker() as session:
            get_booking_query = cls._get_bookings_by_filter_query(
                user_id=user_id,
                id=booking_id,
            )
            booking = await session.execute(get_booking_query)
            return booking.mappings().one_or_none()


class BookingServiceNullPool(BookingService):
    session_maker = async_session_maker_nullpool
