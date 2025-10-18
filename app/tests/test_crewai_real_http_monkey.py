import os
from fastapi.testclient import TestClient
from app.main import app
from app.integrations.crewai_client import CrewAIClient


def test_crewai_real_http_mode_with_monkeypatched_client(monkeypatch):
    # enable real mode + http, but monkeypatch HTTP call to avoid network
    monkeypatch.setenv("CREWAI_MODE", "real")
    monkeypatch.setenv("CREWAI_API_KEY", "dummy-key")
    monkeypatch.setenv("CREWAI_HTTP_MODE", "http")

    def fake_run_node(self, prompt: str, context=None):  # noqa: ANN001
        node = (context or {}).get("node", "?")
        return {"status": "ok", "output": f"http-out-{node}"}

    monkeypatch.setattr(CrewAIClient, "run_node", fake_run_node)

    client = TestClient(app)
    rf = client.post(
        "/flows",
        json={
            "name": "CrewAI Real HTTP Monkey",
            "graph_json": {"nodes": [{"id": "n1"}, {"id": "n2"}], "edges": [{"from": "n1", "to": "n2"}]},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]

    rr = client.post("/orchestrate/run", json={"engine": "crewai", "flow_id": flow_id, "inputs": {}})
    assert rr.status_code == 200
    data = rr.json()
    arts = data["plan"]["artifacts"]
    assert arts["n1"]["output"] == "http-out-n1"
    assert arts["n2"]["output"] == "http-out-n2"

