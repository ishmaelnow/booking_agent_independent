import sqlite3
import random

def create_drivers_table():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            vehicle TEXT,
            plate TEXT,
            phone TEXT,
            email TEXT,
            available BOOLEAN DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()

def add_driver(name, vehicle, plate, phone, email):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO drivers (name, vehicle, plate, phone, email)
        VALUES (?, ?, ?, ?, ?)
    """, (name, vehicle, plate, phone, email))

    conn.commit()
    conn.close()

def get_available_driver():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, vehicle, plate, phone, email
        FROM drivers
        WHERE available = 1
    """)
    drivers = cursor.fetchall()
    conn.close()

    if not drivers:
        return None

    selected = random.choice(drivers)
    return {
        "name": selected[0],
        "vehicle": selected[1],
        "plate": selected[2],
        "phone": selected[3],
        "email": selected[4],
        "eta_minutes": random.randint(5, 12)
    }

def list_available_drivers():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, vehicle, plate
        FROM drivers
        WHERE available = 1
    """)
    drivers = cursor.fetchall()
    conn.close()

    return drivers




def mark_driver_unavailable(name):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE drivers
        SET available = 0
        WHERE name = ?
    """, (name,))
    conn.commit()
    conn.close()