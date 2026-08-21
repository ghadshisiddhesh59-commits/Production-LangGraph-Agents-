from backend.graph.agent_graph import graph


def test_agent_graph():

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 2 + 2?"
                }
            ]
        }
    )

    assert "messages" in result

    assert len(result["messages"]) > 0

    final_message = result["messages"][-1]

    assert final_message.content