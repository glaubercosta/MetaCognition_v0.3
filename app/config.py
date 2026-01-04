import os
from functools import lru_cache



APP_ENV = os.getenv("APP_ENV", "dev").lower()
CREWAI_MODE = os.getenv("CREWAI_MODE", "stub").lower()  # stub | real
CREWAI_API_KEY = os.getenv("CREWAI_API_KEY", "")

DEFAULT_ENGINE = os.getenv("DEFAULT_ENGINE", "langchain").lower()

LANGCHAIN_PROVIDER = os.getenv("LANGCHAIN_PROVIDER", "stub").lower()
LANGCHAIN_MODEL = os.getenv("LANGCHAIN_MODEL", "")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_BASE_URL = os.getenv("LANGCHAIN_BASE_URL", "")
LANGCHAIN_TEMPERATURE = float(os.getenv("LANGCHAIN_TEMPERATURE", "0"))


def _int_from_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed


def import_max_file_mb() -> int:
    """Return the maximum allowed import file size in megabytes (<=0 disables the check)."""
    return _int_from_env("IMPORT_MAX_FILE_MB", 2)


def import_max_items() -> int:
    """Return the maximum number of items accepted in a single import (<=0 disables the check)."""
    return _int_from_env("IMPORT_MAX_ITEMS", 25)


def prompt_max_bytes() -> int:
    """Return the maximum size in bytes accepted for agent prompts (<=0 disables the check)."""
    return _int_from_env("PROMPT_MAX_BYTES", 8192)


def import_max_file_bytes() -> int:
    limit_mb = import_max_file_mb()
    return 0 if limit_mb <= 0 else limit_mb * 1024 * 1024


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
