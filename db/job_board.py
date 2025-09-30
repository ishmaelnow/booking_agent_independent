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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup_location TEXT,
            dropoff_location TEXT,
            fare_estimate TEXT,
            driver_name TEXT,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        SELECT driver_name, pickup_location, dropoff_location, fare_estimate, eta_minutes
        FROM jobs
        WHERE id = ?
    """, (job_id,))
    job = cursor.fetchone()

    if not job:
        print("❌ Job not found.")
        conn.close()
        return None

    assigned_driver = job[0]
    if assigned_driver != driver_name:
        print(f"❌ Driver mismatch: job assigned to {assigned_driver}, not {driver_name}.")
        conn.close()
        return None

    cursor.execute("""
        UPDATE jobs
        SET claimed = 1
        WHERE id = ?
    """, (job_id,))
    conn.commit()
    conn.close()

    return {
        "pickup": job[1],
        "dropoff": job[2],
        "fare": job[3],
        "eta": job[4]
    }

def complete_job(job_id):
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pickup_location, dropoff_location, fare_estimate, driver_name
        FROM jobs
        WHERE id = ?
    """, (job_id,))
    job = cursor.fetchone()

    if job:
        cursor.execute("""
            INSERT INTO completed_jobs (
                pickup_location, dropoff_location, fare_estimate, driver_name
            ) VALUES (?, ?, ?, ?)
        """, (job[0], job[1], job[2], job[3]))

        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))

    conn.commit()
    conn.close()