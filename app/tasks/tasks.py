import smtplib
from datetime import date, timedelta
from pathlib import Path
from typing import Union

from asgiref.sync import async_to_sync
from PIL import Image
from pydantic import EmailStr

from app.bookings.dao import BookingServiceNullPool
from app.bookings.schemas import BookingWithRoomUserInfoSchema
from app.config import settings
from app.email_templates import (
    create_booking_confirmation_template,
    create_booking_reminder_email_one_day_before_checkin_template,
    create_booking_reminder_email_three_days_before_checkin_template,
)
from app.tasks.celery_app import celery_app


@celery_app.task
def process_image(
    path: str,
):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_big = image.resize((1000, 500))
    image_resized_small = image.resize((200, 100))
    image_resized_big.save(f"app/static/images/resized_1000_500_{image_path.name}")
    image_resized_small.save(f"app/static/images/resized_200_100_{image_path.name}")


@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    send_email(
        create_booking_confirmation_template,
        booking,
        email_to,
    )


@celery_app.task
def bulk_send_booking_reminder_email_one_day_before_checkin():
    one_day_before_date_from = date.today() + timedelta(days=1)
    bookings_to_remind = async_to_sync(
        BookingServiceNullPool.get_all_bookings_with_user_info_by_filter
    )(date_from=one_day_before_date_from)
    for booking in bookings_to_remind:
        booking_dict = BookingWithRoomUserInfoSchema.model_validate(booking).model_dump()
        send_booking_reminder_email_one_day_before_checkin_to_one_user.delay(
            booking_dict,
            booking_dict["email"],
        )


@celery_app.task
def bulk_send_booking_reminder_email_three_days_before_checkin():
    three_days_before_date_from = date.today() + timedelta(days=3)
    bookings_to_remind = async_to_sync(
        BookingServiceNullPool.get_all_bookings_with_user_info_by_filter
    )(date_from=three_days_before_date_from)
    for booking in bookings_to_remind:
        booking_dict = BookingWithRoomUserInfoSchema.model_validate(booking).model_dump()
        send_booking_reminder_email_three_days_before_checkin_to_one_user.delay(
            booking_dict,
            booking_dict["email"],
        )


@celery_app.task
def send_booking_reminder_email_one_day_before_checkin_to_one_user(
    booking: dict,
    email_to: EmailStr,
):
    send_email(
        create_booking_reminder_email_one_day_before_checkin_template,
        booking,
        email_to,
    )


@celery_app.task
def send_booking_reminder_email_three_days_before_checkin_to_one_user(
    booking: dict,
    email_to: EmailStr,
):
    send_email(
        create_booking_reminder_email_three_days_before_checkin_template,
        booking,
        email_to,
    )


def send_email(
    create_template_func: Union[
        create_booking_reminder_email_one_day_before_checkin_template,
        create_booking_reminder_email_three_days_before_checkin_template,
        create_booking_confirmation_template,
    ],
    booking: dict,
    email_to: EmailStr,
):
    email_to_mock = settings.SMTP_USER
    email_to = email_to_mock
    message_content = create_template_func(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(message_content)
