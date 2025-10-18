import os
from fastapi.testclient import TestClient
from app.main import app
from app.integrations.crewai_client import CrewAIClient


def test_crewai_real_http_mode_openai_like_response(monkeypatch):
    monkeypatch.setenv("CREWAI_MODE", "real")
    monkeypatch.setenv("CREWAI_API_KEY", "dummy-key")
    monkeypatch.setenv("CREWAI_HTTP_MODE", "http")

    def fake_run_node(self, prompt: str, context=None):  # noqa: ANN001
        node = (context or {}).get("node", "?")
        return {"status": "ok", "output": f"ok-{node}", "error": None}

    monkeypatch.setattr(CrewAIClient, "run_node", fake_run_node)

    client = TestClient(app)
    rf = client.post(
        "/flows",
        json={
            "name": "CrewAI Real HTTP OpenAI-like",
            "graph_json": {"nodes": [{"id": "a"}, {"id": "b"}], "edges": [{"from": "a", "to": "b"}]},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]

    rr = client.post("/orchestrate/run", json={"engine": "crewai", "flow_id": flow_id, "inputs": {"prompt": "X"}})
    assert rr.status_code == 200
    data = rr.json()
    arts = data["plan"]["artifacts"]
    assert arts["a"]["output"] == "ok-a"
    assert arts["b"]["output"] == "ok-b"
