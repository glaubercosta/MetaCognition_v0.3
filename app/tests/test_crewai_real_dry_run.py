import os
from fastapi.testclient import TestClient
from app.main import app


def test_crewai_real_with_key_returns_200(monkeypatch):
    monkeypatch.setenv("CREWAI_MODE", "real")
    monkeypatch.setenv("CREWAI_API_KEY", "dummy-key")
    client = TestClient(app)
    rf = client.post(
        "/flows",
        json={
            "name": "CrewAI Real DryRun",
            "graph_json": {"nodes": [{"id": "x"}, {"id": "y"}], "edges": [{"from": "x", "to": "y"}]},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]
    rr = client.post(
        "/orchestrate/run",
        json={"engine": "crewai", "flow_id": flow_id, "inputs": {"prompt": "Spec"}},
    )
    assert rr.status_code == 200
    data = rr.json()
    assert data["engine"] == "crewai"
    plan = data["plan"]
    assert plan["executed_nodes"] == ["x", "y"]
    assert set(plan["artifacts"].keys()) == {"x", "y"}
