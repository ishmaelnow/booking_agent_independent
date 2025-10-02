import sqlite3
from datetime import datetime

def save_booking(state):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    # ✅ Ensure table includes 'pin' and 'rider_name'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup TEXT,
            dropoff TEXT,
            ride_time TEXT,
            rider_name TEXT,
            phone_number TEXT,
            fare TEXT,
            miles REAL,
            notes TEXT,
            explanation TEXT,
            timestamp TEXT,
            pin TEXT
        )
    """)

    # ✅ Save booking with correct column alignment
    cursor.execute("""
        INSERT INTO bookings (
            pickup, dropoff, ride_time, rider_name,
            phone_number, fare, miles, notes,
            explanation, timestamp, pin
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state["pickup_location"],
        state["dropoff_location"],
        state["ride_time"],
        state.get("rider_name"),  # Optional, defaults to None if missing
        state["phone_number"],
        state["fare_estimate"],
        state["estimated_miles"],
        state["fare_notes"],
        state["fare_explanation"],
        datetime.now().isoformat(),
        str(state["pin"])  # Ensure stored as string
    ))

    conn.commit()
    conn.close()