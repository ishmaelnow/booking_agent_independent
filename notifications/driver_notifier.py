import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

def notify_driver_email(state):
    subject = f"🚕 New Ride Assigned: {state['pickup_location']} → {state['dropoff_location']}"
    body = (
        f"Hello {state['driver_name']},\n\n"
        f"You've been assigned a new ride:\n"
        f"📍 Pickup: {state['pickup_location']}\n"
        f"🏁 Dropoff: {state['dropoff_location']}\n"
        f"🕒 Time: {state['ride_time']}\n"
        f"📞 Rider Phone: {state['phone_number']}\n"
        f"💰 Estimated Fare: ${state['fare_estimate']}\n\n"
        f"Please confirm availability and begin route.\n"
        f"Vehicle: {state['vehicle']} ({state['plate']})\n"
        f"ETA to pickup: {state['eta_minutes']} minutes\n"
    )
    send_email(os.getenv("DRIVER_EMAIL"), subject, body)

def notify_driver_claim(driver_email, job):
    subject = f"✅ Job Claimed: {job['pickup']} → {job['dropoff']}"
    body = (
        f"You have successfully claimed a ride.\n\n"
        f"📍 Pickup: {job['pickup']}\n"
        f"🏁 Dropoff: {job['dropoff']}\n"
        f"💰 Fare: ${job['fare']}\n"
        f"⏱️ ETA: {job['eta']} minutes\n\n"
        f"Please proceed to pickup."
    )
    send_email(driver_email, subject, body)