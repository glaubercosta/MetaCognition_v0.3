from __future__ import annotations

from typing import Dict, Any, List
import json
import datetime
import time

from ...integrations.langchain_messages import SystemMessage, HumanMessage

from ..engine import (
    OrchestratorEngine,
    OrchestrationResult,
    OrchestrationPlan,
    OrchestrationArtifact,
)
from ...services import agents_service
from ...integrations.langchain_client import create_langchain_chat_model
from ...config import langchain_settings


class LangChainEngine(OrchestratorEngine):
    """Engine that executes flows using LangChain chat models."""

    def __init__(self) -> None:
        self._llm = create_langchain_chat_model(langchain_settings())

    def run(self, flow: Dict[str, Any], inputs: Dict[str, Any]) -> OrchestrationResult:
        start = time.perf_counter()
        nodes = flow.get("nodes", []) or []
        logs: List[str] = []

        def log(msg: str, node: str | None = None, payload: Dict[str, Any] | None = None) -> None:
            entry: Dict[str, Any] = {
                "ts": datetime.datetime.now(datetime.UTC).isoformat(),
                "level": "info",
                "engine": "langchain",
                "msg": msg,
            }
            if node:
                entry["node"] = node
            if payload:
                entry.update(payload)
            logs.append(json.dumps(entry, ensure_ascii=False))

        log("LangChain engine: execução iniciada")

        executed: List[str] = []
        artifacts: Dict[str, OrchestrationArtifact] = {}
        previous_outputs: Dict[str, str] = {}

        safe_inputs = inputs or {}

        for node in nodes:
            node_id = node.get("id")
            executed.append(node_id)
            agent_id = node.get("agentId")
            agent = agents_service.get_agent(agent_id) if agent_id else None

            if not agent:
                raise ValueError(f"Agent '{agent_id}' not encontrado para o node '{node_id}'.")

            messages = [
                SystemMessage(
                    content=agent.role
                    or f"Você é o agente '{agent.name}' responsável por processar parte do fluxo."
                ),
                HumanMessage(
                    content=_build_prompt(agent.prompt, safe_inputs, previous_outputs),
                ),
            ]

            try:
                response = self._llm.invoke(messages)
            except Exception as exc:  # pragma: no cover - redepend on provider errors
                raise ValueError(f"Erro ao processar node '{node_id}' com LangChain: {exc}") from exc

            output_text = getattr(response, "content", None) or str(response)
            artifacts[node_id] = OrchestrationArtifact(status="ok", output=output_text)
            previous_outputs[node_id] = output_text
            log(
                "LangChain engine: node executado",
                node=node_id,
                payload={"output_preview": output_text[:128]},
            )

        log("LangChain engine: concluída")

        plan = OrchestrationPlan(executed_nodes=executed, artifacts=artifacts, routing="sequential")
        duration_ms = int((time.perf_counter() - start) * 1000)
        return OrchestrationResult(engine="langchain", flow_id="unknown", plan=plan, logs=logs, duration_ms=duration_ms)


def _build_prompt(agent_prompt: str, inputs: Dict[str, Any], previous_outputs: Dict[str, str]) -> str:
    """Combine stored agent prompt with runtime inputs and previous outputs."""
    safe_prompt = agent_prompt or ""
    sections = [safe_prompt.strip(), ""]
    if inputs:
        try:
            rendered_inputs = json.dumps(inputs, ensure_ascii=False, indent=2)
        except TypeError:
            rendered_inputs = str(inputs)
        sections.append(f"Contexto do fluxo:\n{rendered_inputs}")
    if previous_outputs:
        try:
            rendered_outputs = json.dumps(previous_outputs, ensure_ascii=False, indent=2)
        except TypeError:
            rendered_outputs = str(previous_outputs)
        sections.append(f"Saídas anteriores:\n{rendered_outputs}")
    sections.append("Produza a melhor continuação baseada nas instruções e contexto acima.")
    return "\n\n".join(filter(None, sections))
