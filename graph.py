import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import BookingState
from nodes.generate_booking import generate_booking
from nodes.explain_fare import explain_fare_fn
from dispatch.dispatcher import dispatch_booking
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph

graph = StateGraph(BookingState)

graph.add_node("generate_booking", generate_booking)
graph.add_node("explain_fare", RunnableLambda(explain_fare_fn))
graph.add_node("dispatch", RunnableLambda(dispatch_booking))

graph.add_edge("generate_booking", "explain_fare")
graph.add_edge("explain_fare", "dispatch")

graph.set_entry_point("generate_booking")
graph.set_finish_point("dispatch")
app = graph.compile()