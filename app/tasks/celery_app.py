from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled",
    ],
)


celery_app.conf.beat_schedule = {
    "scheduled_bulk_send_booking_reminder_email_one_day_before_checkin": {
        "task": "scheduled_bulk_send_booking_reminder_email_one_day_before_checkin",
        "schedule": crontab(minute="00", hour="9"),
    },
    "scheduled_bulk_send_booking_reminder_email_three_days_before_checkin": {
        "task": "scheduled_bulk_send_booking_reminder_email_three_days_before_checkin",
        "schedule": crontab(minute="30", hour="15"),
    },
}
