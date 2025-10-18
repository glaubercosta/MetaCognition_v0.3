from typing import Dict, Any
import time, datetime, json
from ..engine import (
    OrchestratorEngine,
    OrchestrationResult,
    OrchestrationPlan,
    OrchestrationArtifact,
)


class CrewAIEngine(OrchestratorEngine):
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        start = time.perf_counter()
        nodes = flow.get("nodes", [])
        logs: list[str] = []

        def log(msg: str, node: str | None = None):
            entry = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), "level": "info", "msg": msg}
            if node:
                entry["node"] = node
            logs.append(json.dumps(entry, ensure_ascii=False))

        log("CrewAI stub: execução iniciada")
        executed: list[str] = []
        artifacts: dict[str, OrchestrationArtifact] = {}
        for n in nodes:
            nid = n.get("id")
            executed.append(nid)
            artifacts[nid] = OrchestrationArtifact(status="ok", output=f"fake-output-{nid}")
            log("CrewAI stub: node executado", node=nid)
        log("CrewAI stub: concluída")
        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        duration_ms = int((time.perf_counter() - start) * 1000)
        return OrchestrationResult(engine="crewai", flow_id="unknown", plan=plan, logs=logs, duration_ms=duration_ms)
