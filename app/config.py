import os
from functools import lru_cache


CREWAI_MODE = os.getenv("CREWAI_MODE", "stub").lower()  # stub | real
CREWAI_API_KEY = os.getenv("CREWAI_API_KEY", "")

DEFAULT_ENGINE = os.getenv("DEFAULT_ENGINE", "langchain").lower()

LANGCHAIN_PROVIDER = os.getenv("LANGCHAIN_PROVIDER", "stub").lower()
LANGCHAIN_MODEL = os.getenv("LANGCHAIN_MODEL", "")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_BASE_URL = os.getenv("LANGCHAIN_BASE_URL", "")
LANGCHAIN_TEMPERATURE = float(os.getenv("LANGCHAIN_TEMPERATURE", "0"))


@lru_cache(maxsize=1)
def langchain_settings() -> dict:
    """Return consolidated settings for the LangChain engine."""
    return {
        "provider": LANGCHAIN_PROVIDER,
        "model": LANGCHAIN_MODEL,
        "api_key": LANGCHAIN_API_KEY,
        "base_url": LANGCHAIN_BASE_URL,
        "temperature": LANGCHAIN_TEMPERATURE,
    }
