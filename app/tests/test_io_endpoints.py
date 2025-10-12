from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_export_agents_json():
    r = client.get("/agents/export?format=json")
    assert r.status_code == 200

def test_export_flows_yaml():
    r = client.get("/flows/export?format=yaml")
    assert r.status_code == 200
    assert "Content-Type" in r.headers
