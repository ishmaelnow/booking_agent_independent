# notifications/driver_notifier.py
# --------------------------------------------------------------
# Purpose: email the driver when a job is assigned/claimed.
# Adds:
#   - env checks (EMAIL_SENDER, EMAIL_PASSWORD, DRIVER_EMAIL)
#   - SMTP_SSL timeout, try/except fail-soft
#   - keeps API flow non-blocking (caller can .spawn/.thread if needed)
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
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use an App Password with Gmail!
DEFAULT_DRIVER_EMAIL = os.getenv("DRIVER_EMAIL")  # optional default

def _send_email(to: str, subject: str, body: str) -> None:
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not to:
        return  # missing config; fail-soft
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception:
        # fail-soft: do not break request handling because SMTP is down
        pass

def notify_driver_email(state: Dict[str, Any], to: str | None = None) -> None:
    to = to or DEFAULT_DRIVER_EMAIL
    if not to:
        return
    subject = f"🚕 New Ride Assigned: {state.get('pickup_location','')} → {state.get('dropoff_location','')}"
    body = (
        f"Hello {state.get('driver_name','Driver')},\n\n"
        f"You've been assigned a new ride:\n"
        f"📍 Pickup: {state.get('pickup_location','')}\n"
        f"🏁 Dropoff: {state.get('dropoff_location','')}\n"
        f"🕒 Time: {state.get('ride_time','')}\n"
        f"📞 Rider Phone: {state.get('phone_number','')}\n"
        f"💰 Estimated Fare: ${state.get('fare_estimate','')}\n\n"
        f"Vehicle: {state.get('vehicle','')} ({state.get('plate','')})\n"
        f"ETA to pickup: {state.get('eta_minutes','')} minutes\n"
    )
    _send_email(to, subject, body)

def notify_driver_claim(driver_email: str, job: Dict[str, Any]) -> None:
    if not driver_email:
        return
    subject = f"✅ Job Claimed: {job.get('pickup','')} → {job.get('dropoff','')}"
    body = (
        f"You have successfully claimed a ride.\n\n"
        f"📍 Pickup: {job.get('pickup','')}\n"
        f"🏁 Dropoff: {job.get('dropoff','')}\n"
        f"💰 Fare: ${job.get('fare','')}\n"
        f"⏱️ ETA: {job.get('eta','')} minutes\n\n"
        f"Please proceed to pickup."
    )
    _send_email(driver_email, subject, body)
