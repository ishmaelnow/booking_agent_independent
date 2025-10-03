import sqlite3

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
            pin TEXT,
            latitude REAL,
            longitude REAL
        )
    """)
    conn.commit()
    conn.close()