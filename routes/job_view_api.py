from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/view")
def view_jobs():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, pickup_location, dropoff_location, fare_estimate, claimed
        FROM jobs
        ORDER BY posted_at DESC
    """)
    jobs = cursor.fetchall()
    conn.close()

    result = []
    for job in jobs:
        result.append({
            "id": job[0],
            "pickup": job[1],
            "dropoff": job[2],
            "fare": job[3],
            "status": "claimed" if job[4] else "available"
        })

    return {"jobs": result}