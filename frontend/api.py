import os
import requests


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


def ask_question(
    question: str,
    session_id: str
):

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "question": question,
            "session_id": session_id
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()