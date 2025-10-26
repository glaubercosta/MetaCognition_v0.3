#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install langchain-openai

export LANGCHAIN_PROVIDER="openai"
export LANGCHAIN_MODEL="${LANGCHAIN_MODEL:-gpt-4o-mini}"
export LANGCHAIN_API_KEY="${LANGCHAIN_API_KEY:-YOUR_OPENAI_KEY}"

echo "LangChain OpenAI configuration ready. Update LANGCHAIN_API_KEY before running the orchestrator."
