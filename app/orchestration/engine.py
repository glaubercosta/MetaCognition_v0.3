from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field


class OrchestrationRequest(BaseModel):
    engine: str = "crewai"
    flow_id: str
    inputs: Dict[str, Any] = Field(default_factory=dict)


class OrchestrationArtifact(BaseModel):
    status: Literal["ok", "error"]
    output: Optional[str] = None
    error: Optional[str] = None


class OrchestrationPlan(BaseModel):
    executed_nodes: List[str]
    artifacts: Dict[str, OrchestrationArtifact]
    routing: Optional[str] = "sequential"


class OrchestrationResult(BaseModel):
    engine: str
    flow_id: str
    plan: OrchestrationPlan
    logs: List[str]
    duration_ms: Optional[int] = None
    request_id: Optional[str] = None


class OrchestratorEngine:
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        raise NotImplementedError
