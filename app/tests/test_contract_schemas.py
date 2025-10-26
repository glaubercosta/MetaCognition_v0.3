import json
from pathlib import Path

from app.models import AgentCreate, FlowCreate
from app.orchestration.engine import OrchestrationRequest, OrchestrationResult


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = ROOT / "ProjectArtifacts" / "schemas"


def _load_schema(name: str) -> dict:
    path = SCHEMAS_DIR / name
    if not path.exists():
        raise AssertionError(f"Schema file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def test_agent_create_schema_up_to_date():
    expected = AgentCreate.model_json_schema()
    assert expected == _load_schema("agent-create.schema.json")


def test_flow_create_schema_up_to_date():
    expected = FlowCreate.model_json_schema()
    assert expected == _load_schema("flow-create.schema.json")


def test_orchestrate_request_schema_up_to_date():
    expected = OrchestrationRequest.model_json_schema()
    assert expected == _load_schema("orchestrate-run-request.schema.json")


def test_orchestrate_response_schema_up_to_date():
    expected = OrchestrationResult.model_json_schema()
    assert expected == _load_schema("orchestrate-run-response.schema.json")
