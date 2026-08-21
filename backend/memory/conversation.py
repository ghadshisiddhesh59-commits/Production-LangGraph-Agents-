from typing import Dict, List


class ConversationMemory:

    def __init__(self):

        self.sessions: Dict[str, List] = {}

    def get_messages(self, session_id: str):

        return self.sessions.get(
            session_id,
            []
        )

    def add_messages(
        self,
        session_id: str,
        messages: list
    ):

        if session_id not in self.sessions:

            self.sessions[session_id] = []

        self.sessions[session_id].extend(
            messages
        )

        return self.sessions[session_id]

    def clear(self, session_id: str):

        self.sessions.pop(
            session_id,
            None
        )