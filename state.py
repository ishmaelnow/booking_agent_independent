from typing import TypedDict

class BookingState(TypedDict, total=False):
    # Booking input
    task: str
    pickup_location: str
    dropoff_location: str
    ride_time: str
    phone_number: str

    # Booking output
    booking_request: str

    # Fare logic
    estimated_miles: float
    fare_estimate: str
    fare_notes: str
    fare_explanation: str

    # Dispatch logic
    dispatch_info: str
    driver_name: str
    vehicle: str
    plate: str
    eta_minutes: int