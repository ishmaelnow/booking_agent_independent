# routes/book.py
# -------------------------------------------------------------------
# POST /book/ride
# GET  /book/history
# - Validates input
# - Persists the job to DB first (so dispatcher can update it)
# - Runs the LangGraph pipeline (generate -> explain -> dispatch)
# - Returns a concise rider-friendly payload (incl. fare fields)
# - Notifications are non-blocking (file log + operator email + driver email)
# -------------------------------------------------------------------

from __future__ import annotations

from typing import List, Dict, Any
from fastapi import APIRouter, Query, BackgroundTasks, status

from state import (
    BookingInput,
    booking_input_to_state,
    merge_state,
)
from graph import run_booking_flow

# ✅ Notifications (all are fail-soft; they won’t break the request)
from notifications.notifier import notify_operator
from notifications.email_notifier import notify_operator_email
from notifications.driver_notifier import notify_driver_email

# Optional DB layer (Postgres helpers); fallback to memory in dev
try:
    # writer provides both create_job() and list_bookings()
    from db.writer import create_job, list_bookings  # from db.writer (not db.reader)
except Exception:
    create_job = None
    list_bookings = None

router = APIRouter(prefix="/book", tags=["book"])

# Dev-only memory fallback store
_FALLBACK_BOOKINGS: List[Dict[str, Any]] = []


def _persist_booking(state: Dict[str, Any]) -> str:
    """
    Persist and return a job_id. Uses DB if present; falls back to memory.
    IMPORTANT: We persist BEFORE running the graph so dispatcher can update the row.
    """
    if create_job:
        try:
            job_id = create_job(state)  # integer id from Postgres
            return str(job_id)
        except Exception:
            # DB failed; fall back to memory
            pass

    job_id = f"JOB-{len(_FALLBACK_BOOKINGS) + 1:06d}"
    row = {**state, "job_id": job_id}
    _FALLBACK_BOOKINGS.append(row)
    return job_id


def _list_bookings(limit: int, offset: int) -> List[Dict[str, Any]]:
    if list_bookings:
        try:
            return list_bookings(limit=limit, offset=offset)
        except Exception:
            pass
    return _FALLBACK_BOOKINGS[offset : offset + limit]


@router.post("/ride", status_code=status.HTTP_201_CREATED)
def create_ride(payload: BookingInput, background: BackgroundTasks):
    """
    Create a new ride:
      1) validate & build state
      2) persist to DB to get job_id (so dispatch can update it)
      3) add a short numeric pin (string; keeps leading zeros)
      4) run the booking graph (generate -> explain -> dispatch)
      5) enqueue notifications (file log + operator email + driver email if assigned)
      6) return a concise rider-facing response (incl. fare fields)
    """
    # 1) Start state from request
    state = booking_input_to_state(payload)

    # 2) Persist first so dispatcher can update jobs table (needs job_id)
    job_id_str = _persist_booking(state)
    state["job_id"] = job_id_str

    # 3) Stable 4–6 digit PIN for tracking (string to keep leading zeros)
    pin = (str(abs(hash(f"{job_id_str}:{state.get('phone_number', '')}")))[-6:]).zfill(4)[:6]
    state["pin"] = pin

    # 4) Run the pipeline (generate_booking -> explain_fare -> dispatch)
    #    If anything raises, return graceful response and keep any fare fields we already computed.
    try:
        state = run_booking_flow(state)
    except Exception as e:
        state = merge_state(
            state,
            {
                "dispatch_info": f"⚠️ Booking saved, but dispatch temporarily unavailable: {e.__class__.__name__}",
                "driver_name": None,
                "vehicle": None,
                "plate": None,
                "eta_minutes": None,
            },
        )

    # 5) Background notifications (best-effort; never block the response)
    #    - operator file log
    #    - operator email (if EMAIL_* configured)
    #    - driver email (only if a driver was assigned; also requires EMAIL_* configured)
    def _notify_async(s: Dict[str, Any]):
        try:
            notify_operator(s)
        except Exception:
            pass
        try:
            notify_operator_email(s)
        except Exception:
            pass
        try:
            if s.get("driver_name"):
                # notify_driver_email uses DRIVER_EMAIL env by default (or you can pass a specific address)
                notify_driver_email(s)
        except Exception:
            pass

    background.add_task(_notify_async, dict(state))

    # 6) Return a concise rider-friendly payload, including fare info
    return {
        "job_id": job_id_str,
        "pin": pin,
        "dispatch_info": state.get("dispatch_info"),
        "driver_name": state.get("driver_name"),
        "vehicle": state.get("vehicle"),
        "plate": state.get("plate"),
        "eta_minutes": state.get("eta_minutes"),
        # Fare fields computed by nodes/explain_fare.py
        "fare_estimate": state.get("fare_estimate"),
        "fare_explanation": state.get("fare_explanation"),
        "estimated_miles": state.get("estimated_miles"),
    }


@router.get("/history")
def view_booking_history(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    Return recent bookings (paginated). Uses DB if available; else memory.
    """
    items = _list_bookings(limit=limit, offset=offset)
    return {"ok": True, "count": len(items), "items": items}
