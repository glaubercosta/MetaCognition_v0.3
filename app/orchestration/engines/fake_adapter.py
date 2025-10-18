from typing import Dict, Any
from ..engine import OrchestratorEngine, OrchestrationResult


class FakeEngine(OrchestratorEngine):
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        # Basic contract validation
        nodes = flow.get("nodes", [])
        if not isinstance(nodes, list):
            raise ValueError("invalid_flow: nodes must be a list")

        # Simulate explicit error via input flag
        if inputs.get("simulate_error"):
            raise ValueError(str(inputs.get("simulate_error")))

        logs = ["[FakeEngine] Execução simulada iniciada."]
        plan = {"executed_nodes": [], "artifacts": {}, "routing": "sequential"}

        base_prompt = inputs.get("prompt", "")

        for n in nodes:
            nid = n.get("id")
            plan["executed_nodes"].append(nid)
            # Deterministic output: echo node id + optional base prompt fragment
            snippet = (base_prompt or "")[:24]
            out = f"fake-{nid}{('-' + snippet) if snippet else ''}"
            plan["artifacts"][nid] = {"status": "ok", "output": out}
            logs.append(f"[FakeEngine] Node {nid} executado.")

        logs.append("[FakeEngine] Concluída.")
        return OrchestrationResult(engine="fake", flow_id="unknown", plan=plan, logs=logs)

