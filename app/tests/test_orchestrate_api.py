from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_flow_and_run():
    flow_payload = {
        "name": "Simple Flow",
        "description": "Test flow",
        "graph_json": {"nodes":[{"id":"a"},{"id":"b"}], "edges":[{"from":"a","to":"b"}]}
    }
    rf = client.post("/flows", json=flow_payload)
    assert rf.status_code == 201
    flow_id = rf.json()["id"]

    rr = client.post("/orchestrate/run", json={"engine":"crewai","flow_id":flow_id,"inputs":{}})
    assert rr.status_code == 200
    data = rr.json()
    assert data["engine"] == "crewai"
    assert len(data["plan"]["executed_nodes"]) == 2
