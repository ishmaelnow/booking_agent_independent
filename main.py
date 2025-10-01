import os
from dotenv import load_dotenv
load_dotenv()

from graph import app
from db.writer import save_booking
from db.job_board import create_jobs_table, post_job
from notifications.email_notifier import notify_operator_email
from notifications.driver_notifier import notify_driver_email

def run_booking_agent():
    print("🚕 Welcome to the Booking Agent")
    name = input("Enter your name: ")  # ✅ NEW
    pickup = input("Enter pickup location: ")
    dropoff = input("Enter dropoff location: ")
    ride_time = input("Enter desired ride time: ")
    phone = input("Enter your phone number: ")

    state = {
        "task": "book a ride",
        "rider_name": name,  # ✅ NEW
        "pickup_location": pickup,
        "dropoff_location": dropoff,
        "ride_time": ride_time,
        "phone_number": phone
    }

    final_state = app.invoke(state)

    print(f"\n✅ Booking confirmed for {final_state['rider_name']}")
    print("🚕 Booking Request:")
    print(final_state["booking_request"])
    print("\n💰 Fare Estimate: $" + final_state["fare_estimate"])
    print("🧾 Fare Notes:", final_state["fare_notes"])
    print("🧠 Fare Explanation:")
    print(final_state["fare_explanation"])
    print("\n🚦 Dispatch Info:")
    print(final_state["dispatch_info"])

    save_booking(final_state)
    notify_operator_email(final_state)
    notify_driver_email(final_state)
    create_jobs_table()
    post_job(final_state)

if __name__ == "__main__":
    run_booking_agent()