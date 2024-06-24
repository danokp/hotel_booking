import pytest
from fastapi import status


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status_code",
    [
        *[(4, "2025-05-01", "2025-05-15", status.HTTP_200_OK)] * 8,
        (4, "2025-05-01", "2025-05-15", status.HTTP_409_CONFLICT),
        (4, "2025-05-01", "2025-05-15", status.HTTP_409_CONFLICT),
    ],
)
async def test_add_and_get_booking(
    room_id: int,
    date_from: str,
    date_to: str,
    status_code: int,
    authenticated_async_client,
    mocker,
):
    send_booking_notification_email = mocker.patch(
        "app.tasks.tasks.send_booking_confirmation_email.delay"
    )

    bookings_before_adding = await authenticated_async_client.get("/bookings")
    bookings_before_adding_count = len(bookings_before_adding.json())
    response = await authenticated_async_client.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code

    bookings_after_adding = await authenticated_async_client.get("/bookings")
    bookings_after_adding_count = len(bookings_after_adding.json())
    if status_code == status.HTTP_200_OK:
        assert bookings_after_adding_count == bookings_before_adding_count + 1
        assert send_booking_notification_email.called
    else:
        assert bookings_after_adding_count == bookings_before_adding_count
        assert not send_booking_notification_email.called
