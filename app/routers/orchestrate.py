from fastapi import APIRouter, HTTPException
from ..orchestration.engine import OrchestrationRequest, OrchestrationResult
from ..services import flows_service as flows
from ..orchestration.engines.crewai_adapter import CrewAIEngine
from ..orchestration.engines.robotgreen_adapter import RobotGreenEngine

router = APIRouter(prefix="/orchestrate", tags=["orchestrate"])

@router.post("/run", response_model=OrchestrationResult)
def run(req: OrchestrationRequest):
    f = flows.get_flow(req.flow_id)
    if not f:
        raise HTTPException(404, "Flow not found")
    if req.engine.lower() == "crewai":
        runner = CrewAIEngine()
    elif req.engine.lower() == "robotgreen":
        runner = RobotGreenEngine()
    else:
        raise HTTPException(400, "Unsupported engine")
    result = runner.run(f.graph_json, req.inputs)
    result.flow_id = f.id  # type: ignore
    return result
