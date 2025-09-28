import os
from dotenv import load_dotenv
load_dotenv()

from graph import app
from db.writer import save_booking
from notifications.email_notifier import notify_operator_email

def run_booking_agent():
    print("🚕 Welcome to the Booking Agent")
    pickup = input("Enter pickup location: ")
    dropoff = input("Enter dropoff location: ")
    ride_time = input("Enter desired ride time: ")
    phone = input("Enter your phone number: ")

    state = {
        "task": "book a ride",
        "pickup_location": pickup,
        "dropoff_location": dropoff,
        "ride_time": ride_time,
        "phone_number": phone
    }

    final_state = app.invoke(state)

    print("\n🚕 Booking Request:")
    print(final_state["booking_request"])
    print("\n💰 Fare Estimate: $" + final_state["fare_estimate"])
    print("🧾 Fare Notes:", final_state["fare_notes"])
    print("🧠 Fare Explanation:")
    print(final_state["fare_explanation"])

    save_booking(final_state)
    notify_operator_email(final_state)

if __name__ == "__main__":
    run_booking_agent()