from typing import Dict, Any
from ..engine import (
    OrchestratorEngine,
    OrchestrationResult,
    OrchestrationPlan,
    OrchestrationArtifact,
)


class CrewAIEngine(OrchestratorEngine):
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        nodes = flow.get("nodes", [])
        logs = ["[CrewAI] Simulação iniciada."]
        executed: list[str] = []
        artifacts: dict[str, OrchestrationArtifact] = {}
        for n in nodes:
            nid = n.get("id")
            executed.append(nid)
            artifacts[nid] = OrchestrationArtifact(status="ok", output=f"fake-output-{nid}")
            logs.append(f"[CrewAI] Node {nid} executado.")
        logs.append("[CrewAI] Concluída.")
        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        return OrchestrationResult(engine="crewai", flow_id="unknown", plan=plan, logs=logs)

