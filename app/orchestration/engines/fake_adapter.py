from typing import Dict, Any
import time, datetime, json
from ..engine import (
    OrchestratorEngine,
    OrchestrationResult,
    OrchestrationPlan,
    OrchestrationArtifact,
)


class FakeEngine(OrchestratorEngine):
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        # Basic contract validation
        nodes = flow.get("nodes", [])
        if not isinstance(nodes, list):
            raise ValueError("invalid_flow: nodes must be a list")

        # Simulate explicit error via input flag
        if inputs.get("simulate_error"):
            raise ValueError(str(inputs.get("simulate_error")))

        start = time.perf_counter()
        logs: list[str] = []

        def log(msg: str, node: str | None = None):
            entry = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), "level": "info", "msg": msg}
            if node:
                entry["node"] = node
            logs.append(json.dumps(entry, ensure_ascii=False))

        log("FakeEngine: execução simulada iniciada")
        executed: list[str] = []
        artifacts: dict[str, OrchestrationArtifact] = {}

        base_prompt = inputs.get("prompt", "")

        for n in nodes:
            nid = n.get("id")
            executed.append(nid)
            # Deterministic output: echo node id + optional base prompt fragment
            snippet = (base_prompt or "")[:24]
            out = f"fake-{nid}{('-' + snippet) if snippet else ''}"
            artifacts[nid] = OrchestrationArtifact(status="ok", output=out)
            log("FakeEngine: node executado", node=nid)

        log("FakeEngine: concluída")
        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        duration_ms = int((time.perf_counter() - start) * 1000)
        return OrchestrationResult(engine="fake", flow_id="unknown", plan=plan, logs=logs, duration_ms=duration_ms)
