from sqlalchemy.orm import Session

from backend.database.models import ConversationMessage


class MemoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_messages(self, session_id: str):

        records = (
            self.db.query(ConversationMessage)
            .filter(
                ConversationMessage.session_id == session_id
            )
            .order_by(
                ConversationMessage.created_at
            )
            .all()
        )

        return [
            {
                "role": record.role,
                "content": record.content
            }
            for record in records
        ]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        message = ConversationMessage(
            session_id=session_id,
            role=role,
            content=content
        )

        self.db.add(message)
        self.db.commit()

        return message