# notifications/email_notifier.py
# --------------------------------------------------------------
# Purpose: email the operator on new bookings.
# Same env/timeouts/fail-soft safeguards as driver_notifier.
# --------------------------------------------------------------

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # required for operator email

def notify_operator_email(state: Dict[str, Any]) -> None:
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        return  # missing config → no-op

    msg = EmailMessage()
    msg["Subject"] = f"🚕 New Booking: {state.get('pickup_location','')} → {state.get('dropoff_location','')}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    body = (
        f"📍 Pickup: {state.get('pickup_location','')}\n"
        f"🏁 Dropoff: {state.get('dropoff_location','')}\n"
        f"🕒 Time: {state.get('ride_time','')}\n"
        f"📞 Phone: {state.get('phone_number','')}\n"
        f"💰 Fare: ${state.get('fare_estimate','')}\n"
        f"🧾 Notes: {state.get('fare_notes','')}\n"
        f"🧠 Explanation:\n{state.get('fare_explanation','')}"
    )
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception:
        # fail-soft
        pass
