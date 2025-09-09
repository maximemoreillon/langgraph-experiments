from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def dummy_node(state: State):
    return {"messages": state["messages"]}


graph_builder.add_node("start_node", dummy_node)
graph_builder.add_node("second_node", dummy_node)

graph_builder.add_edge(START, "start_node")
graph_builder.add_edge("start_node", "second_node")

graph = graph_builder.compile()


print(graph.get_graph().draw_ascii())


response = graph.invoke({"messages": ["message 1", "message 2"]})
print(response)
