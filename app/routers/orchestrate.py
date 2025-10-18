from fastapi import APIRouter, HTTPException
from ..orchestration.engine import OrchestrationRequest, OrchestrationResult
from ..services import flows_service as flows
from ..orchestration.engines.crewai_adapter import CrewAIEngine
from ..orchestration.engines.robotgreen_adapter import RobotGreenEngine
from ..orchestration.engines.fake_adapter import FakeEngine
from ..orchestration.engines.crewai_real import RealCrewAIEngine
import os
import uuid, json, datetime

router = APIRouter(prefix="/orchestrate", tags=["orchestrate"])

@router.post("/run", response_model=OrchestrationResult)
def run(req: OrchestrationRequest):
    f = flows.get_flow(req.flow_id)
    if not f:
        raise HTTPException(404, "Flow not found")
    if req.engine.lower() == "crewai":
        crewai_mode = os.getenv("CREWAI_MODE", "stub").lower()
        crewai_api_key = os.getenv("CREWAI_API_KEY", "")
        if crewai_mode == "real":
            if not crewai_api_key:
                raise HTTPException(501, "CrewAI real adapter disabled or CREWAI_API_KEY not set")
            runner = RealCrewAIEngine()
        else:
            runner = CrewAIEngine()
    elif req.engine.lower() == "robotgreen":
        runner = RobotGreenEngine()
    elif req.engine.lower() == "fake":
        runner = FakeEngine()
    else:
        raise HTTPException(400, "Unsupported engine")
    try:
        result = runner.run(f.graph_json, req.inputs)
    except ValueError as e:
        raise HTTPException(400, f"Engine error: {e}")
    except NotImplementedError as e:
        raise HTTPException(501, str(e))
    result.flow_id = f.id  # type: ignore

    # Enrich logs with request_id, engine and flow_id and append a summary event
    request_id = str(uuid.uuid4())
    enriched_logs = []
    for line in (result.logs or []):  # type: ignore
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                obj["request_id"] = request_id
                obj["engine"] = result.engine
                obj["flow_id"] = f.id
                enriched_logs.append(json.dumps(obj, ensure_ascii=False))
            else:
                raise ValueError("non-dict")
        except Exception:
            enriched_logs.append(
                json.dumps(
                    {
                        "ts": datetime.datetime.now(datetime.UTC).isoformat(),
                        "level": "info",
                        "msg": str(line),
                        "request_id": request_id,
                        "engine": result.engine,
                        "flow_id": f.id,
                    },
                    ensure_ascii=False,
                )
            )

    summary = {
        "ts": datetime.datetime.now(datetime.UTC).isoformat(),
        "level": "info",
        "msg": "orchestration_summary",
        "request_id": request_id,
        "engine": result.engine,
        "flow_id": f.id,
        "duration_ms": result.duration_ms,
        "executed_nodes": len(result.plan.executed_nodes),  # type: ignore
        "artifacts": len(result.plan.artifacts),  # type: ignore
    }
    enriched_logs.append(json.dumps(summary, ensure_ascii=False))
    result.logs = enriched_logs  # type: ignore
    return result
