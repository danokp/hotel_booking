from datetime import date

from fastapi import APIRouter, Depends
from fastapi_versioning import version

from app.bookings.dao import BookingService
from app.bookings.schemas import BookingWithRoomInfoSchema
from app.exceptions import (
    BookingCannotBeDeletedException,
    BookingCannotBeFoundException,
    RoomCannotBeBookedException,
)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Hotel booking"],
)


@router.get("")
@version(1)
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[BookingWithRoomInfoSchema]:
    return await BookingService.get_all_bookings_for_user_by_filter(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
) -> BookingWithRoomInfoSchema:
    new_booking_id = await BookingService.add(user.id, room_id, date_from, date_to)
    if not new_booking_id:
        raise RoomCannotBeBookedException

    new_booking_with_room_info = await BookingService.get(
        booking_id=new_booking_id, user_id=user.id
    )
    booking_dict = BookingWithRoomInfoSchema.model_validate(
        new_booking_with_room_info
    ).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)

    return new_booking_with_room_info


@router.get("/{booking_id}")
@version(1)
async def get_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
) -> BookingWithRoomInfoSchema:
    booking = await BookingService.get(booking_id=booking_id, user_id=user.id)
    if not booking:
        raise BookingCannotBeFoundException
    return booking


@router.delete("/{booking_id}")
@version(1)
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    deleted_booking = await BookingService.delete(booking_id=booking_id, user_id=user.id)
    if not deleted_booking:
        raise BookingCannotBeDeletedException
