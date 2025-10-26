#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install langchain-community

export LANGCHAIN_PROVIDER="ollama"
export LANGCHAIN_MODEL="${LANGCHAIN_MODEL:-llama3.1}"
export LANGCHAIN_BASE_URL="${LANGCHAIN_BASE_URL:-http://localhost:11434}"

echo "LangChain Ollama configuration ready. Ensure Ollama is running locally before executing the orchestrator."
