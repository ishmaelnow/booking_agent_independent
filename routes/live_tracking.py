from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
import psycopg2

router = APIRouter()

def get_db():
    conn = psycopg2.connect(
        dbname="booking_agent",
        user="postgres",
        password="somepassword",  # replace with your actual password
        host="localhost",
        port="5432"
    )
    return conn

def get_latest_location(pin: int, role: str, conn) -> dict | None:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT
              ST_Y(location::geometry) AS lat,
              ST_X(location::geometry) AS lng,
              timestamp
            FROM locations
            WHERE pin = %s AND role = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """, (pin, role))
        result = cursor.fetchone()
        return result if result else None

@router.get("/track/live")
def get_live_locations(pin: int):
    conn = get_db()
    try:
        driver = get_latest_location(pin=pin, role="driver", conn=conn)
        rider = get_latest_location(pin=pin, role="rider", conn=conn)

        response = {}
        if driver:
            response["driver"] = driver
        if rider:
            response["rider"] = rider

        if not response:
            return {"status": "empty", "detail": "No live location available for this pin."}

        return response
    finally:
        conn.close()