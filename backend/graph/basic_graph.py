from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


class State(TypedDict):
    message: object


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def llm_node(state: State):

    response = llm.invoke(state["message"])

    return {
        "message": response.content
    }


graph_builder = StateGraph(State)

graph_builder.add_node(
    "llm",
    llm_node
)

graph_builder.add_edge(
    START,
    "llm"
)

graph_builder.add_edge(
    "llm",
    END
)

graph = graph_builder.compile()


result = graph.invoke(
    {
        "message": "Explain what a Large Language Model is in simple words."
    }
)

print(result)