import sqlite3

def create_jobs_table():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup_location TEXT,
            dropoff_location TEXT,
            ride_time TEXT,
            phone_number TEXT,
            fare_estimate TEXT,
            fare_notes TEXT,
            fare_explanation TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            claimed BOOLEAN DEFAULT 0,
            driver_name TEXT,
            vehicle TEXT,
            plate TEXT,
            eta_minutes INTEGER
        )
    """)

    conn.commit()
    conn.close()

def post_job(state):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (
            pickup_location, dropoff_location, ride_time, phone_number,
            fare_estimate, fare_notes, fare_explanation,
            driver_name, vehicle, plate, eta_minutes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state["pickup_location"],
        state["dropoff_location"],
        state["ride_time"],
        state["phone_number"],
        state["fare_estimate"],
        state["fare_notes"],
        state["fare_explanation"],
        state["driver_name"],
        state["vehicle"],
        state["plate"],
        state["eta_minutes"]
    ))

    conn.commit()
    conn.close()

def claim_job(job_id, driver_name):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET claimed = 1
        WHERE id = ? AND driver_name = ?
    """, (job_id, driver_name))

    conn.commit()

    cursor.execute("""
        SELECT pickup_location, dropoff_location, fare_estimate, eta_minutes
        FROM jobs
        WHERE id = ?
    """, (job_id,))
    job = cursor.fetchone()

    conn.close()

    if job:
        return {
            "pickup": job[0],
            "dropoff": job[1],
            "fare": job[2],
            "eta": job[3]
        }
    return None






def claim_job(job_id, driver_name):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET claimed = 1
        WHERE id = ? AND driver_name = ?
    """, (job_id, driver_name))

    conn.commit()

    cursor.execute("""
        SELECT pickup_location, dropoff_location, fare_estimate, eta_minutes
        FROM jobs
        WHERE id = ?
    """, (job_id,))
    job = cursor.fetchone()

    conn.close()

    if job:
        return {
            "pickup": job[0],
            "dropoff": job[1],
            "fare": job[2],
            "eta": job[3]
        }
    return None