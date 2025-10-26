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

        def log(msg: str, node: str | None = None) -> None:
            entry = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), "level": "info", "msg": msg}
            if node:
                entry["node"] = node
            logs.append(json.dumps(entry, ensure_ascii=False))

        log(f"CrewAI REAL: execucao iniciada ({mode})")
        executed: list[str] = []
        artifacts: dict[str, OrchestrationArtifact] = {}
        safe_inputs = {k: v for k, v in (inputs or {}).items() if not k.startswith("_")}
        prompt_snippet = (safe_inputs.get("prompt") or "")[:48]
        flow_meta = inputs.get("_flow_meta") or {}
        client = CrewAIClient(
            api_key=os.getenv("CREWAI_API_KEY", ""),
            base_url=os.getenv("CREWAI_BASE_URL", "https://api.crewai.example"),
            timeout_sec=int(os.getenv("CREWAI_TIMEOUT_SEC", "30")),
            max_retries=int(os.getenv("CREWAI_MAX_RETRIES", "2")),
            backoff_sec=float(os.getenv("CREWAI_BACKOFF_SEC", "0.5")),
        )

        model = os.getenv("CREWAI_MODEL", "crewai-large")

        def build_prompt_for_node(nid: str) -> str:
            base = safe_inputs.get("prompt") or ""
            ctx = safe_inputs.get("context") or {}
            return f"[model:{model}] node:{nid} {base} ctx:{list(ctx.keys())}"

        for node in nodes:
            node_id = node.get("id")
            executed.append(node_id)
            if mode == "http":
                node_params = node.get("params") or {}
                resp = client.run_node(
                    prompt=build_prompt_for_node(node_id),
                    context={
                        "node": node_id,
                        "model": model,
                        "flow_nodes": len(nodes),
                        "edges": flow.get("edges", []),
                        "parameters": node_params,
                        "inputs": safe_inputs,
                        "metadata": {
                            "node": node_id,
                            "flow": {
                                "id": flow_meta.get("id"),
                                "name": flow_meta.get("name"),
                                "size": len(nodes),
                            },
                            "prompt_snippet": prompt_snippet,
                        },
                    },
                )
            else:
                resp = client.simulate(node_id, prompt_snippet)
            status = resp.get("status", "ok")
            if status != "ok":
                raise ValueError(resp.get("error") or "crew_error")
            artifacts[node_id] = OrchestrationArtifact(status=status, output=resp.get("output"))
            usage = resp.get("usage")
            if usage:
                log(json.dumps({"usage": usage}), node=node_id)
            log(f"CrewAI REAL: node executado ({mode})", node=node_id)
        log(f"CrewAI REAL: concluida ({mode})")
        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        duration_ms = int((time.perf_counter() - start) * 1000)
        return OrchestrationResult(engine="crewai", flow_id="unknown", plan=plan, logs=logs, duration_ms=duration_ms)
