from typing import TypedDict, Optional

class BookingState(TypedDict, total=False):
    task: str
    pickup_location: str
    dropoff_location: str
    ride_time: str
    phone_number: str

    booking_request: Optional[str]
    estimated_miles: Optional[float]
    fare_estimate: Optional[str]
    fare_notes: Optional[str]
    fare_explanation: Optional[str]