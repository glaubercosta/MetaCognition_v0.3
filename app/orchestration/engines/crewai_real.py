from typing import Dict, Any
import os
from ..engine import (
    OrchestratorEngine,
    OrchestrationResult,
    OrchestrationPlan,
    OrchestrationArtifact,
)
from ...integrations.crewai_client import CrewAIClient


class RealCrewAIEngine(OrchestratorEngine):
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        # Dry-run implementation: produce deterministic outputs while preserving contract
        nodes = flow.get("nodes", [])
        mode = os.getenv("CREWAI_HTTP_MODE", "dry-run").lower()
        logs = [f"[CrewAI REAL] Execução iniciada ({mode})."]
        executed: list[str] = []
        artifacts: dict[str, OrchestrationArtifact] = {}
        prompt_snippet = (inputs.get("prompt") or "")[:24]
        client = CrewAIClient(
            api_key=os.getenv("CREWAI_API_KEY", ""),
            base_url=os.getenv("CREWAI_BASE_URL", "https://api.crewai.example"),
        )
        for n in nodes:
            nid = n.get("id")
            executed.append(nid)
            if mode == "http":
                # Compose a minimal prompt; real impl would build from agent/flow context
                resp = client.run_node(
                    prompt=f"node:{nid} {prompt_snippet}",
                    context={"node": nid, "flow_nodes": len(nodes)},
                )
            else:
                resp = client.simulate(nid, prompt_snippet)
            status = resp.get("status", "ok")
            if status != "ok":
                # Surface engine error to orchestrate router (HTTP 400)
                raise ValueError(resp.get("error") or "crew_error")
            artifacts[nid] = OrchestrationArtifact(status=status, output=resp.get("output"))
            logs.append(f"[CrewAI REAL] Node {nid} executado ({mode}).")
        logs.append(f"[CrewAI REAL] Concluída ({mode}).")
        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        return OrchestrationResult(engine="crewai", flow_id="unknown", plan=plan, logs=logs)
