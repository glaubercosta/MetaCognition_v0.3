from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _create_simple_flow():
    flow_payload = {
        "name": "Contract Flow",
        "description": "Fake engine contract test",
        "graph_json": {"nodes": [{"id": "n1"}, {"id": "n2"}], "edges": [{"from": "n1", "to": "n2"}]},
    }
    rf = client.post("/flows", json=flow_payload)
    assert rf.status_code == 201
    return rf.json()["id"]


def test_fake_engine_success_contract():
    flow_id = _create_simple_flow()
    rr = client.post(
        "/orchestrate/run",
        json={"engine": "fake", "flow_id": flow_id, "inputs": {"prompt": "Generate specs"}},
    )
    assert rr.status_code == 200
    data = rr.json()
    assert data["engine"] == "fake"
    assert data["flow_id"] == flow_id
    assert "plan" in data and "logs" in data
    plan = data["plan"]
    assert plan["routing"] == "sequential"
    assert plan["executed_nodes"] == ["n1", "n2"]
    assert set(plan["artifacts"].keys()) == {"n1", "n2"}
    assert plan["artifacts"]["n1"]["status"] == "ok"
    assert plan["artifacts"]["n2"]["status"] == "ok"


def test_fake_engine_reports_error():
    flow_id = _create_simple_flow()
    rr = client.post(
        "/orchestrate/run",
        json={"engine": "fake", "flow_id": flow_id, "inputs": {"simulate_error": "invalid_prompt"}},
    )
    # Expect 400 with our error mapping
    assert rr.status_code == 400
    assert "invalid_prompt" in rr.text

