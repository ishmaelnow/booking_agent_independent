from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2

router = APIRouter()

class LocationPayload(BaseModel):
    pin: int
    role: str           # 'driver' or 'rider'
    lat: float
    lng: float

@router.post("/track/location")
def track_location(payload: LocationPayload):
    try:
        conn = psycopg2.connect(
            dbname="booking_agent",
            user="postgres",
            password="somepassword",  # replace with your actual password
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO locations (pin, role, location, timestamp)
            VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), now())
        """, (
            payload.pin,
            payload.role,
            payload.lng,  # X = longitude
            payload.lat   # Y = latitude
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print("TRACK LOCATION ERROR:", str(e))  # Optional: log to console
        raise HTTPException(status_code=500, detail=str(e))