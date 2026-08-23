from backend.graph.agent_graph import graph
from backend.database.connection import SessionLocal
from backend.memory.repository import MemoryRepository
from backend.logger import logger


class AgentService:

    def __init__(self):
        self.graph = graph

    def ask(
        self,
        question: str,
        session_id: str
    ):
        logger.info(
            f"Agent request | session_id={session_id}"
        )

        db = SessionLocal()

        try:
            memory = MemoryRepository(db)

            history = memory.get_messages(
                session_id
            )

            messages = history + [
                {
                    "role": "user",
                    "content": question
                }
            ]

            result = self.graph.invoke(
                {
                    "messages": messages
                }
            )

            response = result["messages"][-1]

            full_response = response.content

            if isinstance(full_response, list):
                full_response = "".join(
                    block.get("text", "")
                    for block in full_response
                    if isinstance(block, dict)
                )

            memory.add_message(
                session_id,
                "user",
                question
            )

            memory.add_message(
                session_id,
                "assistant",
                full_response
            )

            logger.info(
                f"Agent response generated | session_id={session_id}"
            )

            return full_response

        except Exception:
            logger.exception(
                f"Agent request failed | session_id={session_id}"
            )
            raise

        finally:
            db.close()

    def stream(
        self,
        question: str,
        session_id: str
    ):
        db = SessionLocal()

        try:
            memory = MemoryRepository(db)

            history = memory.get_messages(
                session_id
            )

            messages = history + [
                {
                    "role": "user",
                    "content": question
                }
            ]

            full_response = ""

            for chunk in self.graph.stream(
                {
                    "messages": messages
                },
                stream_mode="updates"
            ):

                if "agent" not in chunk:
                    continue

                messages_update = chunk["agent"].get(
                    "messages",
                    []
                )

                if not messages_update:
                    continue

                response = messages_update[-1]

                content = response.content

                if isinstance(content, list):
                    content = "".join(
                        block.get("text", "")
                        for block in content
                        if isinstance(block, dict)
                    )

                if content:
                    full_response += content
                    yield content

            memory.add_message(
                session_id,
                "user",
                question
            )

            memory.add_message(
                session_id,
                "assistant",
                full_response
            )

        except Exception:
            logger.exception(
                f"Agent streaming failed | session_id={session_id}"
            )
            raise

        finally:
            db.close()