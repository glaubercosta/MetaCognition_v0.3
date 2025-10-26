from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import os

from .langchain_messages import AIMessage


class StubChatModel:
    """Deterministic chat model used for tests and offline development."""

    def __init__(self, label: str = "stub", temperature: float = 0.0) -> None:
        self.label = label
        self.temperature = temperature

    def invoke(self, messages: Any, **kwargs: Any) -> AIMessage:
        # Derive a short description from the last user message when available
        content = ""
        try:
            if isinstance(messages, list) and messages:
                last = messages[-1]
                content = getattr(last, "content", "") or str(last)
        except Exception:
            content = ""
        text = f"[{self.label} | temp={self.temperature}] {content[:64]}".strip()
        return AIMessage(content=text or f"[{self.label}] response")


@dataclass
class LangChainProviderSettings:
    provider: str
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.0


def _create_openai(settings: LangChainProviderSettings):
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "LangChain provider 'openai' requires the 'langchain-openai' package. "
            "Install it with `pip install langchain-openai`."
        ) from exc

    api_key = settings.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY or LANGCHAIN_API_KEY must be set for provider 'openai'.")

    return ChatOpenAI(
        model=settings.model or "gpt-4o-mini",
        api_key=api_key,
        base_url=settings.base_url or None,
        temperature=settings.temperature,
    )


def _create_google_gemini(settings: LangChainProviderSettings):
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "LangChain provider 'google-gemini' requires the 'langchain-google-genai' package. "
            "Install it with `pip install langchain-google-genai`."
        ) from exc

    api_key = settings.api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY or LANGCHAIN_API_KEY must be set for provider 'google-gemini'.")

    return ChatGoogleGenerativeAI(
        model=settings.model or "gemini-1.5-pro",
        google_api_key=api_key,
        temperature=settings.temperature,
    )


def _create_ollama(settings: LangChainProviderSettings):
    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "LangChain provider 'ollama' requires the 'langchain-community' package. "
            "Install it with `pip install langchain-community`."
        ) from exc

    model = settings.model or "llama3.1"
    base_url = settings.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return ChatOllama(model=model, base_url=base_url, temperature=settings.temperature)


PROVIDER_FACTORIES = {
    "stub": lambda settings: StubChatModel(label="langchain-stub", temperature=settings.temperature),
    "openai": _create_openai,
    "google-gemini": _create_google_gemini,
    "ollama": _create_ollama,
}


def create_langchain_chat_model(settings: Dict[str, Any]):
    """Create a LangChain chat model based on the provided settings dictionary."""
    provider_settings = LangChainProviderSettings(
        provider=(settings.get("provider") or "stub").lower(),
        model=settings.get("model") or None,
        api_key=settings.get("api_key") or None,
        base_url=settings.get("base_url") or None,
        temperature=float(settings.get("temperature") or 0.0),
    )

    factory = PROVIDER_FACTORIES.get(provider_settings.provider)
    if not factory:
        raise RuntimeError(
            f"Unsupported LangChain provider '{provider_settings.provider}'. "
            f"Supported providers: {', '.join(PROVIDER_FACTORIES.keys())}"
        )
    return factory(provider_settings)
