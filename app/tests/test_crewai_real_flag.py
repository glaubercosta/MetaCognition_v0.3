import os
from fastapi.testclient import TestClient
from app.main import app


def test_crewai_real_without_key_returns_501(monkeypatch):
    monkeypatch.setenv("CREWAI_MODE", "real")
    if "CREWAI_API_KEY" in os.environ:
        monkeypatch.delenv("CREWAI_API_KEY", raising=False)
    client = TestClient(app)
    # create simple flow
    rf = client.post(
        "/flows",
        json={
            "name": "CrewAI Real Flag",
            "graph_json": {"nodes": [{"id": "a"}], "edges": []},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]
    # run orchestration with crewai
    rr = client.post("/orchestrate/run", json={"engine": "crewai", "flow_id": flow_id, "inputs": {}})
    assert rr.status_code == 501
    assert "CREWAI" in rr.text or "adapter" in rr.text

