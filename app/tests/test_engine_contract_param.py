import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_flow(nodes=2):
    graph_nodes = [{"id": f"n{i+1}"} for i in range(nodes)]
    graph_edges = [
        {"from": f"n{i+1}", "to": f"n{i+2}"} for i in range(nodes - 1)
    ]
    rf = client.post(
        "/flows",
        json={
            "name": f"Contract Flow x{nodes}",
            "description": "Param engine contract test",
            "graph_json": {"nodes": graph_nodes, "edges": graph_edges},
        },
    )
    assert rf.status_code == 201
    return rf.json()["id"], [n["id"] for n in graph_nodes]


@pytest.mark.parametrize("engine", ["fake", "crewai", "robotgreen"])
def test_engine_contract_success(engine):
    flow_id, node_ids = create_flow(3)
    rr = client.post("/orchestrate/run", json={"engine": engine, "flow_id": flow_id, "inputs": {}})
    assert rr.status_code == 200
    data = rr.json()
    assert data["engine"] == engine
    assert data["flow_id"] == flow_id
    plan = data["plan"]
    assert plan["routing"] == "sequential"
    assert plan["executed_nodes"] == node_ids
    assert set(plan["artifacts"].keys()) == set(node_ids)
    # artifacts have status ok
    for aid, art in plan["artifacts"].items():
        assert art["status"] == "ok"


@pytest.mark.parametrize("engine", ["fake"])  # only fake supports simulate_error
def test_engine_contract_error(engine):
    flow_id, _ = create_flow(2)
    rr = client.post(
        "/orchestrate/run",
        json={"engine": engine, "flow_id": flow_id, "inputs": {"simulate_error": "invalid_prompt"}},
    )
    assert rr.status_code == 400
    assert "invalid_prompt" in rr.text

