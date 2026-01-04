import json
from pathlib import Path
from app.models import AgentCreate, FlowCreate
from app.orchestration.engine import OrchestrationRequest, OrchestrationResult

ROOT = Path(__file__).resolve().parent
SCHEMAS_DIR = ROOT / "ProjectArtifacts" / "schemas"
SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

def save_schema(model, filename):
    schema = model.model_json_schema()
    path = SCHEMAS_DIR / filename
    path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"Updated {path}")

if __name__ == "__main__":
    save_schema(AgentCreate, "agent-create.schema.json")
    save_schema(FlowCreate, "flow-create.schema.json")
    save_schema(OrchestrationRequest, "orchestrate-run-request.schema.json")
    save_schema(OrchestrationResult, "orchestrate-run-response.schema.json")
