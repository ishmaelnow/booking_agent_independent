def calculate_base_fare(miles: float) -> float:
    base_fare = 3.00
    per_mile_rate = 4.00
    multiplier = 0.70  # dynamic pricing factor

    fare = base_fare + (miles * per_mile_rate * multiplier)
    return round(fare, 2)