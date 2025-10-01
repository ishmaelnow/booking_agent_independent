from fastapi import APIRouter, Request, Query, HTTPException
from typing import Optional
from graph import app as dispatch_graph
from db.writer import save_booking
from db.job_board import create_jobs_table, post_job
from db.reader import load_bookings  # ✅ For history filtering
from notifications.email_notifier import notify_operator_email
from notifications.driver_notifier import notify_driver_email
from resources.fare_utils import explain_fare  # ✅ Fare logic

router = APIRouter(prefix="/book", tags=["Booking"])

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

# ✅ Privacy-aware booking history endpoint
@router.get("/history")
def view_booking_history(phone_number: Optional[str] = Query(None)):
    if not phone_number:
        raise HTTPException(status_code=400, detail="Missing phone_number")

    all_bookings = load_bookings()
    filtered = [b for b in all_bookings if b.get("phone_number") == phone_number]
    return {"bookings": filtered}