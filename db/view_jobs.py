import sqlite3

def view_jobs():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, pickup_location, dropoff_location, fare_estimate, claimed FROM jobs ORDER BY posted_at DESC")
    jobs = cursor.fetchall()

    for job in jobs:
        status = "✅ Claimed" if job[4] else "🆕 Available"
        print(f"[{job[0]}] {job[1]} → {job[2]} | Fare: ${job[3]} | {status}")

    conn.close()

if __name__ == "__main__":
    view_jobs()