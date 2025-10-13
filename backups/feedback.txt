from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
import sqlite3

from db.reader import load_bookings  # ✅ For PIN validation

router = APIRouter(prefix="/book", tags=["Booking"])  # ✅ Consistent with booking routes

@router.post("/feedback")
async def submit_feedback(request: Request):
    state = await request.json()
    state["task"] = "submit feedback"

    # ✅ Enforce required fields
    if "feedback_rating" not in state:
        raise HTTPException(status_code=400, detail="Missing feedback_rating")
    if "feedback_comments" not in state:
        raise HTTPException(status_code=400, detail="Missing feedback_comments")
    if "pin" not in state:
        raise HTTPException(status_code=400, detail="Missing PIN")

    # ✅ Extract and sanitize fields
    pin = str(state["pin"]).strip()
    rating = int(state["feedback_rating"])
    comments = state["feedback_comments"].strip()
    timestamp = datetime.utcnow().isoformat()
    ip = request.client.host

    # ✅ Validate PIN against existing bookings
    bookings = load_bookings()
    if not any(str(b.get("pin", "")).strip() == pin for b in bookings):
        raise HTTPException(status_code=403, detail="Invalid PIN")

    # ✅ Save feedback to SQLite
    try:
        conn = sqlite3.connect("booking_agent.db")
        cursor = conn.cursor()

        # ✅ Ensure feedback table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pin TEXT,
                rating INTEGER,
                comments TEXT,
                timestamp TEXT,
                ip TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO feedback (pin, rating, comments, timestamp, ip)
            VALUES (?, ?, ?, ?, ?)
        """, (pin, rating, comments, timestamp, ip))

        conn.commit()
        return {
            "confirmation": f"✅ Feedback recorded for PIN {pin}",
            "feedback": {
                "rating": rating,
                "comments": comments,
                "timestamp": timestamp
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        conn.close()