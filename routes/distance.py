from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2

router = APIRouter()

# Payload schema: expects a pin to identify the user/session
class DistancePayload(BaseModel):
    pin: int

# Route: calculates distance between the two most recent locations for a given pin
@router.post("/distance")
def calculate_distance(payload: DistancePayload):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="booking_agent",
            user="postgres",
            password="somepassword",  # replace with actual password
            host="localhost"
        )
        cur = conn.cursor()

        # SQL: fetches the two most recent location points and computes distance
        cur.execute("""
            SELECT ST_Distance(
                (SELECT location FROM locations WHERE pin = %s ORDER BY timestamp DESC LIMIT 1 OFFSET 1),
                (SELECT location FROM locations WHERE pin = %s ORDER BY timestamp DESC LIMIT 1)
            );
        """, (payload.pin, payload.pin))

        result = cur.fetchone()
        cur.close()
        conn.close()

        # If distance is computable, return it; else raise 404
        if result and result[0] is not None:
            return {"distance_meters": result[0]}
        else:
            raise HTTPException(status_code=404, detail="Not enough location data to calculate distance.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))