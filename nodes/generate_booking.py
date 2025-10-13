# nodes/generate_booking.py
# --------------------------------------------------------------
# Purpose: produce a human-friendly booking summary string.
# --------------------------------------------------------------

from typing import Dict, Any

def generate_booking(state: Dict[str, Any]) -> Dict[str, Any]:
    pickup = (state.get("pickup_location") or "").strip()
    dropoff = (state.get("dropoff_location") or "").strip()
    ride_time = (state.get("ride_time") or "").strip()
    phone = (state.get("phone_number") or "").strip()

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
