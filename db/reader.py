import sqlite3

def load_bookings():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, pickup, dropoff, ride_time, rider_name, phone_number,
               fare, miles, notes, explanation, timestamp
        FROM bookings
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "pickup": r[1],
            "dropoff": r[2],
            "ride_time": r[3],
            "rider_name": r[4],
            "phone_number": r[5],
            "fare": r[6],
            "miles": r[7],
            "notes": r[8],
            "explanation": r[9],
            "timestamp": r[10]
        }
        for r in rows
    ]