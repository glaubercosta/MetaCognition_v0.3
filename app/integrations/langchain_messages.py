from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:  # Prefer the real LangChain message implementations when available.
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  # type: ignore
except ImportError:  # Fallback used during tests or when LangChain is not installed.
    @dataclass
    class _BaseMessage:
        content: Any

        def __str__(self) -> str:
            return str(self.content)

    class SystemMessage(_BaseMessage):
        ...

    class HumanMessage(_BaseMessage):
        ...

    class AIMessage(_BaseMessage):
        ...

__all__ = ["AIMessage", "HumanMessage", "SystemMessage"]
