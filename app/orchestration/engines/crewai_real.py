from typing import Dict, Any
import os, time, datetime, json
from ..engine import (
    OrchestratorEngine,
    OrchestrationResult,
    OrchestrationPlan,
    OrchestrationArtifact,
)
from ...integrations.crewai_client import CrewAIClient


class RealCrewAIEngine(OrchestratorEngine):
    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        nodes = flow.get("nodes", [])
        mode = os.getenv("CREWAI_HTTP_MODE", "dry-run").lower()
        start = time.perf_counter()
        logs: list[str] = []

        def log(msg: str, node: str | None = None):
            entry = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), "level": "info", "msg": msg}
            if node:
                entry["node"] = node
            logs.append(json.dumps(entry, ensure_ascii=False))

        log(f"CrewAI REAL: execução iniciada ({mode})")
        executed: list[str] = []
        artifacts: dict[str, OrchestrationArtifact] = {}
        prompt_snippet = (inputs.get("prompt") or "")[:48]
        client = CrewAIClient(
            api_key=os.getenv("CREWAI_API_KEY", ""),
            base_url=os.getenv("CREWAI_BASE_URL", "https://api.crewai.example"),
        )

        model = os.getenv("CREWAI_MODEL", "crewai-large")

        def build_prompt_for_node(nid: str) -> str:
            base = inputs.get("prompt") or ""
            ctx = inputs.get("context") or {}
            return f"[model:{model}] node:{nid} {base} ctx:{list(ctx.keys())}"

        for n in nodes:
            nid = n.get("id")
            executed.append(nid)
            if mode == "http":
                resp = client.run_node(
                    prompt=build_prompt_for_node(nid),
                    context={"node": nid, "model": model, "flow_nodes": len(nodes), "edges": flow.get("edges", []), "parameters": inputs.get("parameters", {})},
                )
            else:
                resp = client.simulate(nid, prompt_snippet)
            status = resp.get("status", "ok")
            if status != "ok":
                raise ValueError(resp.get("error") or "crew_error")
            artifacts[nid] = OrchestrationArtifact(status=status, output=resp.get("output"))
            log(f"CrewAI REAL: node executado ({mode})", node=nid)
        log(f"CrewAI REAL: concluída ({mode})")
        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        duration_ms = int((time.perf_counter() - start) * 1000)
        return OrchestrationResult(engine="crewai", flow_id="unknown", plan=plan, logs=logs, duration_ms=duration_ms)


