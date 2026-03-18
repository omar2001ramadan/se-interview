from fastapi.testclient import TestClient

from travel_assistant.api import create_app


class FakeAgent:
    def invoke(self, payload):
        message = payload["messages"][0].content
        return {"messages": [type("Message", (), {"content": f"Echo: {message}"})()]}


def test_health_endpoint_returns_ok():
    client = TestClient(create_app(agent_executor=FakeAgent()))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_preserves_contract():
    client = TestClient(create_app(agent_executor=FakeAgent()))
    response = client.post("/chat", json={"message": "Plan a day in Chicago"})
    assert response.status_code == 200
    assert response.json() == {"response": "Echo: Plan a day in Chicago"}
