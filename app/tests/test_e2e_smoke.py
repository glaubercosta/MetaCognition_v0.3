from fastapi.testclient import TestClient
from app.main import app


def test_e2e_create_agent_flow_and_run_fake():
    client = TestClient(app)

    # Create agent
    ra = client.post(
        "/agents",
        json={
            "name": "Spec Analyst",
            "role": "Analista",
            "prompt": "Gerar requisitos",
        },
    )
    assert ra.status_code == 201
    agent_id = ra.json()["id"]
    assert agent_id

    # Create flow
    rf = client.post(
        "/flows",
        json={
            "name": "E2E Flow",
            "graph_json": {"nodes": [{"id": "n1"}, {"id": "n2"}], "edges": [{"from": "n1", "to": "n2"}]},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]

    # Run orchestrate with fake engine
    rr = client.post(
        "/orchestrate/run",
        json={"engine": "fake", "flow_id": flow_id, "inputs": {"prompt": "Specs"}},
    )
    assert rr.status_code == 200
    data = rr.json()
    assert data["engine"] == "fake"
    assert data["flow_id"] == flow_id
    assert isinstance(data.get("request_id"), str) and len(data["request_id"]) > 0
    assert isinstance(data.get("duration_ms"), int)
    plan = data["plan"]
    assert plan["executed_nodes"] == ["n1", "n2"]
    assert set(plan["artifacts"].keys()) == {"n1", "n2"}
