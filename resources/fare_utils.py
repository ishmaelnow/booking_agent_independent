from geopy.distance import geodesic
import geocoder
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def estimate_miles(pickup: str, dropoff: str) -> float:
    try:
        p = geocoder.osm(pickup, headers={"User-Agent": "booking-agent"})
        d = geocoder.osm(dropoff, headers={"User-Agent": "booking-agent"})
        if p.ok and d.ok:
            return round(geodesic((p.lat, p.lng), (d.lat, d.lng)).miles, 2)
    except Exception:
        pass
    return 10.0

def calculate_base_fare(miles: float) -> float:
    base_fare = 3.00
    per_mile_rate = 4.00
    multiplier = 0.70
    return round(base_fare + (miles * per_mile_rate * multiplier), 2)

llm = ChatOpenAI()
fare_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant explaining taxi fare estimates."),
    ("human", "Explain why the fare from {pickup} to {dropoff} is ${fare}. Notes: {notes}.")
])
fare_chain = fare_prompt | llm

def explain_fare(state: dict) -> dict:
    pickup = state["pickup_location"]
    dropoff = state["dropoff_location"]
    miles = estimate_miles(pickup, dropoff)
    fare = calculate_base_fare(miles)
    notes = "Standard metered fare applied"

    explanation = fare_chain.invoke({
        "pickup": pickup,
        "dropoff": dropoff,
        "fare": fare,
        "notes": notes
    }).content

    return {
        **state,
        "estimated_miles": miles,
        "fare_estimate": f"{fare:.2f}",
        "fare_notes": notes,
        "fare_explanation": explanation
    }