from datetime import datetime

from app.bookings.dao import BookingService


async def test_add_and_get_booking():
    new_booking_id = await BookingService.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2024-07-01", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-07-14", "%Y-%m-%d"),
    )
    assert isinstance(new_booking_id, int)

    found_booking = await BookingService.find_by_id(new_booking_id)
    assert found_booking.id == new_booking_id
    assert found_booking.user_id == 2
    assert found_booking.room_id == 2
