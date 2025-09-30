from fastapi import APIRouter, Request

from graph import app as dispatch_graph
from db.writer import save_booking
from db.job_board import create_jobs_table, post_job
from notifications.email_notifier import notify_operator_email
from notifications.driver_notifier import notify_driver_email
from resources.fare_utils import explain_fare  # ✅ Shared logic

router = APIRouter(prefix="/book", tags=["Booking"])

@router.post("/ride")
async def book_ride(request: Request):
    state = await request.json()
    state["task"] = "book a ride"

    state = explain_fare(state)  # ✅ Inject fare logic
    final_state = dispatch_graph.invoke(state)

    save_booking(final_state)
    notify_operator_email(final_state)
    notify_driver_email(final_state)
    create_jobs_table()
    post_job(final_state)

    return final_state