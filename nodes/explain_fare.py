from dotenv import load_dotenv
load_dotenv()

from resources.geo_utils import estimate_miles
from resources.fare_engine import calculate_base_fare
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI()

fare_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant explaining taxi fare estimates."),
    ("human", "Explain why the fare from {pickup} to {dropoff} is ${fare}. Notes: {notes}.")
])

fare_chain = fare_prompt | llm

def explain_fare_fn(state):
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