from backend.database.connection import SessionLocal
from backend.memory.repository import MemoryRepository

def test_memeory():

    db = SessionLocal()

    try:

        memory = MemoryRepository(db)

        session_id = "test_session_001"

        memory.add_message(
            session_id,
            "user",
            "My name is Siddhesh."
        )

        memory.add_message(
            session_id,
            "assistant",
            "Nice to meet you, Siddhesh!"
        )

        messages = memory.get_messages(
            session_id
        )

        assert len(messages) >= 2

        assert messages[-2]["content"] == (
            "My name is Siddhesh."
        )

        assert messages[-1]["content"] == (
            "Nice to meet you, Siddhesh!"
        )

    finally:

        db.close