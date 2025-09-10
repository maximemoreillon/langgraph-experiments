from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    count: int


def dummy_node(state: State):
    newCount = state["count"] + 1
    print(f"Count is now: {newCount}")
    return {"messages": state["messages"], "count": newCount}


def true_node(state: State):
    print(f"Traversed true node")
    return state


def false_node(state: State):
    print(f"Traversed false node")
    return state


def routing_function(state: State):
    return state["count"] > 1


graph_builder = StateGraph(State)

graph_builder.add_node("start_node", dummy_node)
graph_builder.add_node("second_node", dummy_node)
graph_builder.add_node("true_node", true_node)
graph_builder.add_node("false_node", false_node)
graph_builder.add_node("last_node", dummy_node)

graph_builder.add_edge(START, "start_node")
graph_builder.add_edge("start_node", "second_node")

graph_builder.add_edge("true_node", "last_node")
graph_builder.add_edge("false_node", "last_node")


graph_builder.add_conditional_edges(
    "second_node", routing_function, {True: "true_node", False: "false_node"}
)


graph_builder.add_edge("last_node", END)

graph = graph_builder.compile()


print(graph.get_graph().draw_ascii())

response = graph.invoke({"messages": ["message 1", "message 2"], "count": 0})
print(response["messages"])
