from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from backend.agent.agent import Agent
from backend.agent.tools import TOOLS


class State(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]


agent = Agent()


def agent_node(state: State):

    response = agent.run(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(TOOLS)


def route_after_agent(state: State):

    last_message = state["messages"][-1]

    # If the LLM requested one or more tools,
    # send execution to the ToolNode.
    if getattr(
        last_message,
        "tool_calls",
        None
    ):

        return "tools"

    # Otherwise, the LLM has produced
    # the final answer.
    return END


graph_builder = StateGraph(State)


graph_builder.add_node(
    "agent",
    agent_node
)

graph_builder.add_node(
    "tools",
    tool_node
)


graph_builder.add_edge(
    START,
    "agent"
)


graph_builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        END: END
    }
)


graph_builder.add_edge(
    "tools",
    "agent"
)


graph = graph_builder.compile()


if __name__ == "__main__":

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 25 * 48?"
                }
            ]
        }
    )

    print(
        result["messages"][-1].content
    )