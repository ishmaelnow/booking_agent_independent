import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def notify_operator_email(state):
    msg = EmailMessage()
    msg["Subject"] = f"🚕 New Booking: {state['pickup_location']} → {state['dropoff_location']}"
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = os.getenv("EMAIL_RECEIVER")

    body = (
        f"📍 Pickup: {state['pickup_location']}\n"
        f"🏁 Dropoff: {state['dropoff_location']}\n"
        f"🕒 Time: {state['ride_time']}\n"
        f"📞 Phone: {state['phone_number']}\n"
        f"💰 Fare: ${state['fare_estimate']}\n"
        f"🧾 Notes: {state['fare_notes']}\n"
        f"🧠 Explanation:\n{state['fare_explanation']}"
    )
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)