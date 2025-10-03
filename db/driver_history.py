from fastapi import APIRouter, Query
import sqlite3

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.get("/history")
def get_driver_history(driver_name: str = Query(...)):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pickup_location, dropoff_location, fare_estimate, completed_at
        FROM completed_jobs
        WHERE driver_name = ?
        ORDER BY completed_at DESC
    """, (driver_name,))
    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "pickup": r[0],
            "dropoff": r[1],
            "fare": r[2],
            "completed_at": r[3]
        }
        for r in rows
    ]

    return {"driver_name": driver_name, "history": history}