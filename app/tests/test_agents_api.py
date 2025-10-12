from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_agent():
    payload = {
        "name": "Requirements Agent",
        "role": "Requisitos",
        "prompt": "Atue como analista de requisitos",
        "input_artifacts": {"in": ["brief.md"]},
        "output_artifacts": {"out": ["requirements.json"]}
    }
    r = client.post("/agents", json=payload)
    assert r.status_code == 201
    agent_id = r.json()["id"]

    r2 = client.get(f"/agents/{agent_id}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Requirements Agent"
