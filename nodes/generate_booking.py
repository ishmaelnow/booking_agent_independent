# nodes/generate_booking.py

def generate_booking(state):
    pickup = state["pickup_location"]
    dropoff = state["dropoff_location"]
    ride_time = state["ride_time"]
    phone = state["phone_number"]

    request = (
        f"📍 Pickup: {pickup}\n"
        f"🏁 Dropoff: {dropoff}\n"
        f"🕒 Time: {ride_time}\n"
        f"📞 Phone: {phone}"
    )

    return {
        **state,
        "booking_request": request
    }