from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_ask():

    response = client.post(
        "/ask",
        json={
            "question": "What is 2 + 2?",
            "session_id": "api_test_001"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200