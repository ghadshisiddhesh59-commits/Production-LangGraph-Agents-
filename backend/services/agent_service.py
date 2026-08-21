from backend.agent.agent import Agent
from backend.database.connection import SessionLocal
from backend.memory.repository import MemoryRepository
from backend.logger import logger

class AgentService:

    def __init__(self):

        self.agent = Agent()

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

            full_response = ""

            for chunk in self.agent.stream(
                messages
            ):

                if chunk.content:

                    full_response += chunk.content

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

            for chunk in self.agent.stream(
                messages
            ):

                if chunk.content:

                    full_response += chunk.content

                    yield chunk.content

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

        finally:

            db.close()