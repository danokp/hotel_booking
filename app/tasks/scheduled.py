from app.tasks.celery_app import celery_app
from app.tasks.tasks import (
    bulk_send_booking_reminder_email_one_day_before_checkin,
    bulk_send_booking_reminder_email_three_days_before_checkin,
)


@celery_app.task(
    name="scheduled_bulk_send_booking_reminder_email_one_day_before_checkin"
)
def scheduled_bulk_send_booking_reminder_email_one_day_before_checkin():
    bulk_send_booking_reminder_email_one_day_before_checkin.delay()


@celery_app.task(
    name="scheduled_bulk_send_booking_reminder_email_three_days_before_checkin"
)
def scheduled_bulk_send_booking_reminder_email_three_days_before_checkin():
    bulk_send_booking_reminder_email_three_days_before_checkin.delay()
