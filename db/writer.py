import sqlite3
from datetime import datetime

def save_booking(state):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup TEXT,
            dropoff TEXT,
            ride_time TEXT,
            phone_number TEXT,
            fare TEXT,
            miles REAL,
            notes TEXT,
            explanation TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO bookings (
            pickup, dropoff, ride_time, phone_number,
            fare, miles, notes, explanation, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state["pickup_location"],
        state["dropoff_location"],
        state["ride_time"],
        state["phone_number"],
        state["fare_estimate"],
        state["estimated_miles"],
        state["fare_notes"],
        state["fare_explanation"],
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()