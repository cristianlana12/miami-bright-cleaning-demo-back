# backend/app/notifications.py

import smtplib
import requests
from email.message import EmailMessage
from app.config import settings


STATUS_MESSAGES = {
    "pending": {
        "subject": "Your cleaning request was received",
        "message": "Your cleaning request was received successfully. Our team will review it and contact you soon.",
    },
    "confirmed": {
        "subject": "Your cleaning request was confirmed",
        "message": "Great news! Your cleaning request was confirmed. Our team will arrive on the scheduled date and time.",
    },
    "cancelled": {
        "subject": "Your cleaning request was cancelled",
        "message": "Your cleaning request was cancelled. If this was a mistake, please contact us to schedule a new service.",
    },
    "completed": {
        "subject": "Your cleaning service was completed",
        "message": "Your cleaning service was marked as completed. Thank you for choosing Miami Bright Cleaning.",
    },
}


SERVICE_LABELS = {
    "house_cleaning": "House Cleaning",
    "deep_cleaning": "Deep Cleaning",
    "office_cleaning": "Office Cleaning",
    "move_in_out": "Move In / Move Out",
    "airbnb_cleaning": "Airbnb Cleaning",
    "post_construction": "Post Construction",
}


def build_notification_text(booking: dict, status: str) -> tuple[str, str]:
    status_data = STATUS_MESSAGES[status]
    service_name = SERVICE_LABELS.get(booking.get("service_type"), booking.get("service_type"))

    subject = status_data["subject"]

    body = f"""
Hi {booking.get("full_name")},

{status_data["message"]}

Booking details:
Service: {service_name}
Date: {booking.get("booking_date")}
Time: {booking.get("booking_time")}
Address: {booking.get("address")}

Estimated starting price: ${booking.get("estimated_price", "")}

Miami Bright Cleaning
"""

    return subject, body


def send_email(to_email: str, subject: str, body: str) -> None:
    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_password:
        print("Email not configured. Skipping email notification.")
        return

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from or settings.smtp_user
    message["To"] = to_email
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(message)


def send_whatsapp(phone: str, body: str) -> None:
    if not settings.whatsapp_enabled:
        print("WhatsApp disabled. Skipping WhatsApp notification.")
        return

    if not settings.whatsapp_api_url or not settings.whatsapp_token:
        print("WhatsApp not configured. Skipping WhatsApp notification.")
        return

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "to": phone,
        "message": body,
    }

    response = requests.post(
        settings.whatsapp_api_url,
        json=payload,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()


def notify_customer(booking: dict, status: str) -> None:
    subject, body = build_notification_text(booking, status)

    send_email(
        to_email=booking["email"],
        subject=subject,
        body=body,
    )

    send_whatsapp(
        phone=booking["phone"],
        body=body,
    )