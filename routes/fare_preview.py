from fastapi import APIRouter, Query
from resources.fare_utils import calculate_base_fare
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

router = APIRouter(prefix="/fare", tags=["Fare Preview"])

llm = ChatOpenAI()
fare_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant providing short, practical fare summaries."),
    ("human", "Give a concise explanation for a taxi fare of ${fare} based on {miles} miles. Emphasize that this is only an estimate and actual cost may vary due to traffic, tolls, and time.")
])
fare_chain = fare_prompt | llm

@router.get("/estimate")
def estimate_fare(miles: float = Query(..., gt=0)):
    fare = calculate_base_fare(miles)
    notes = "Standard metered fare applied"

    explanation = fare_chain.invoke({
        "miles": miles,
        "fare": fare
    }).content

    return {
        "input_miles": miles,
        "fare_estimate": f"{fare:.2f}",
        "fare_notes": notes,
        "fare_explanation": explanation
    }