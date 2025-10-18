import os
from fastapi.testclient import TestClient
from app.main import app
from app.integrations.crewai_client import CrewAIClient


def test_crewai_real_http_mode_engine_error(monkeypatch):
    monkeypatch.setenv("CREWAI_MODE", "real")
    monkeypatch.setenv("CREWAI_API_KEY", "dummy-key")
    monkeypatch.setenv("CREWAI_HTTP_MODE", "http")

    def fake_run_node(self, prompt: str, context=None):  # noqa: ANN001
        return {"status": "error", "error": "invalid_prompt"}

    monkeypatch.setattr(CrewAIClient, "run_node", fake_run_node)

    client = TestClient(app)
    rf = client.post(
        "/flows",
        json={
            "name": "CrewAI Real HTTP Error Monkey",
            "graph_json": {"nodes": [{"id": "n1"}], "edges": []},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]
    rr = client.post("/orchestrate/run", json={"engine": "crewai", "flow_id": flow_id, "inputs": {}})
    assert rr.status_code == 400
    assert "invalid_prompt" in rr.text

