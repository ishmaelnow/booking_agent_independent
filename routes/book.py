from fastapi import APIRouter, Request, Query, HTTPException
from typing import Optional
from graph import app as dispatch_graph
from db.writer import save_booking
from db.job_board import create_jobs_table, post_job
from db.reader import load_bookings  # ✅ For history filtering
from notifications.email_notifier import notify_operator_email
from notifications.driver_notifier import notify_driver_email
from resources.fare_utils import explain_fare  # ✅ Fare logic
import random  # ✅ Added for PIN generation

router = APIRouter(prefix="/book", tags=["Booking"])

# ✅ Helper: Generate a secure 6-digit integer PIN
def generate_pin():
    return random.randint(100000, 999999)

@router.post("/ride")
async def book_ride(request: Request):
    state = await request.json()
    state["task"] = "book a ride"

    # ✅ Enforce required fields
    if "phone_number" not in state:
        raise HTTPException(status_code=400, detail="Missing phone_number")
    if "rider_name" not in state:
        raise HTTPException(status_code=400, detail="Missing rider_name")

    state = explain_fare(state)  # Inject fare logic
    state["pin"] = generate_pin()  # ✅ Inject secure integer PIN

    final_state = dispatch_graph.invoke(state)

    save_booking(final_state)
    notify_operator_email(final_state)
    notify_driver_email(final_state)
    create_jobs_table()
    post_job(final_state)

    return {
        "confirmation": f"✅ Booking confirmed for {final_state['rider_name']}",
        "booking": final_state
    }

# ✅ Privacy-aware booking history endpoint with PIN verification
@router.get("/history")
def view_booking_history(
    pin: Optional[str] = Query(None)  # ✅ Accept PIN as string
):
    if not pin:
        raise HTTPException(status_code=400, detail="Missing PIN")

    all_bookings = load_bookings()

    # 🔍 Logging for debug
    print("🔐 Incoming PIN:", pin, type(pin))
    if all_bookings:
        print("📦 Sample booking row:", all_bookings[0])
    else:
        print("⚠️ No bookings found in database.")

    # ✅ Type-safe filtering by PIN only
    filtered = [
        b for b in all_bookings
        if str(b.get("pin", "")).strip() == str(pin).strip()
    ]

    if not filtered:
        print("🚫 No matching bookings found for provided PIN.")
        raise HTTPException(status_code=403, detail="Invalid PIN")

    print(f"✅ Found {len(filtered)} matching booking(s).")
    return {"bookings": filtered}