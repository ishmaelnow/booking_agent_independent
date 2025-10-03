from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
import sqlite3  # or use your preferred DB

router = APIRouter()

class Feedback(BaseModel):
    rideId: str | None = None
    rating: int
    comments: str

@router.post("/api/feedback")
async def submit_feedback(feedback: Feedback, request: Request):
    timestamp = datetime.utcnow().isoformat()
    ip = request.client.host

    # Save to DB (example: SQLite)
    conn = sqlite3.connect("fairfare.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (ride_id, rating, comments, timestamp, ip)
        VALUES (?, ?, ?, ?, ?)
    """, (feedback.rideId, feedback.rating, feedback.comments, timestamp, ip))
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Feedback submitted"}