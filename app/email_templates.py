from email.message import EmailMessage
from pathlib import Path

from jinja2 import Template
from pydantic import EmailStr

from app.config import settings


def create_email_template(
    email_template_path: str,
    email_to: EmailStr,
    email_from: EmailStr,
    email_subject: str,
    email_content: dict,
):
    email = EmailMessage()
    email["Subject"] = email_subject
    email["From"] = email_from
    email["To"] = email_to

    email_template_path = Path(email_template_path)
    with open(email_template_path) as html_file:
        template_content = html_file.read()

    template = Template(template_content)
    rendered_template = template.render(**email_content)
    email.set_content(rendered_template, subtype="html")
    return email


def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,
):
    return create_email_template(
        email_template_path="app/templates/emails/booking_confirmation.html",
        email_to=email_to,
        email_from=settings.SMTP_USER,
        email_subject="Booking confirmation",
        email_content={"booking": booking},
    )


def create_booking_reminder_email_one_day_before_checkin_template(
    booking: dict,
    email_to: EmailStr,
):
    return create_email_template(
        email_template_path="app/templates/emails/booking_reminder_one_day_before_checkin.html",
        email_to=email_to,
        email_from=settings.SMTP_USER,
        email_subject="Booking reminder (checkin in one day)",
        email_content={"booking": booking},
    )


def create_booking_reminder_email_three_days_before_checkin_template(
    booking: dict,
    email_to: EmailStr,
):
    return create_email_template(
        email_template_path="app/templates/emails/booking_reminder_three_days_before_checkin.html",
        email_to=email_to,
        email_from=settings.SMTP_USER,
        email_subject="Booking reminder (checkin in three days)",
        email_content={"booking": booking},
    )
