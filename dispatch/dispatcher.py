from db.driver_registry import get_available_driver

def dispatch_booking(state):
    driver = get_available_driver()
    if not driver:
        return {
            **state,
            "dispatch_info": "❌ No available drivers at the moment.",
            "driver_name": None,
            "vehicle": None,
            "plate": None,
            "eta_minutes": None
        }

    dispatch_info = (
        f"🚗 Driver Assigned: {driver['name']} ({driver['vehicle']}, {driver['plate']})\n"
        f"⏱️ ETA: {driver['eta_minutes']} minutes"
    )

    return {
        **state,
        "dispatch_info": dispatch_info,
        "driver_name": driver["name"],
        "vehicle": driver["vehicle"],
        "plate": driver["plate"],
        "eta_minutes": driver["eta_minutes"]
    }