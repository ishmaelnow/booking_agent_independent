from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/view")
def view_bookings():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, pickup, dropoff, ride_time, phone_number, fare, miles, notes, explanation, timestamp
        FROM bookings
        ORDER BY timestamp DESC
    """)
    bookings = cursor.fetchall()
    conn.close()

    result = []
    for b in bookings:
        result.append({
            "id": b[0],
            "pickup": b[1],
            "dropoff": b[2],
            "ride_time": b[3],
            "phone": b[4],
            "fare": b[5],
            "miles": b[6],
            "notes": b[7],
            "explanation": b[8],
            "timestamp": b[9]
        })

    return {"bookings": result}