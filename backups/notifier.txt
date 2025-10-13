from datetime import datetime

def notify_operator(state):
    message = (
        f"[{datetime.now().isoformat()}] NEW BOOKING\n"
        f"📍 Pickup: {state['pickup_location']}\n"
        f"🏁 Dropoff: {state['dropoff_location']}\n"
        f"🕒 Time: {state['ride_time']}\n"
        f"📞 Phone: {state['phone_number']}\n"
        f"💰 Fare: ${state['fare_estimate']}\n"
        f"🧾 Notes: {state['fare_notes']}\n"
        "-----------------------------\n"
    )

    with open("notifications.log", "a") as f:
        f.write(message)