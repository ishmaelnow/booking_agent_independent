import sqlite3
from db.job_board import claim_job, complete_job
from db.driver_registry import mark_driver_unavailable, mark_driver_available

def list_available_jobs():
    conn = sqlite3.connect("booking_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, pickup_location, dropoff_location, ride_time,
               fare_estimate, driver_name, vehicle, plate, eta_minutes
        FROM jobs
        WHERE claimed = 0
        ORDER BY posted_at DESC
    """)
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print("🚫 No available jobs at the moment.")
        return

    print("🧭 Available Jobs:\n")
    for job in jobs:
        print(f"[{job[0]}] {job[1]} → {job[2]} @ {job[3]}")
        print(f"💰 Fare: ${job[4]}")
        print(f"🚗 Driver: {job[5]} ({job[6]}, {job[7]})")
        print(f"⏱️ ETA: {job[8]} minutes")
        print("-" * 40)

def prompt_claim():
    driver_name = input("\nEnter your name to claim a job: ").strip()
    job_id = input("Enter job ID to claim: ").strip()

    if not job_id.isdigit():
        print("❌ Invalid job ID.")
        return

    print(f"🔍 Attempting to claim job ID {job_id} for driver '{driver_name}'")

    job = claim_job(int(job_id), driver_name)
    if job:
        mark_driver_unavailable(driver_name)
        print(f"✅ Job {job_id} claimed by {driver_name}")
        print(f"📍 Pickup: {job['pickup']} → 🏁 Dropoff: {job['dropoff']}")
        print(f"💰 Fare: ${job['fare']} | ⏱️ ETA: {job['eta']} minutes")
    else:
        print("❌ Job not found or driver mismatch.")

def prompt_complete():
    driver_name = input("\nEnter your name to complete a job: ").strip()
    job_id = input("Enter job ID to complete: ").strip()

    if not job_id.isdigit():
        print("❌ Invalid job ID.")
        return

    complete_job(int(job_id))
    mark_driver_available(driver_name)
    print(f"✅ Job {job_id} marked complete and archived. {driver_name} is now available.")

if __name__ == "__main__":
    list_available_jobs()
    prompt_claim()
    prompt_complete()