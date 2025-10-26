#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install langchain-google-genai

export LANGCHAIN_PROVIDER="google-gemini"
export LANGCHAIN_MODEL="${LANGCHAIN_MODEL:-gemini-1.5-pro}"
export LANGCHAIN_API_KEY="${LANGCHAIN_API_KEY:-YOUR_GOOGLE_API_KEY}"

echo "LangChain Google Gemini configuration ready. Update LANGCHAIN_API_KEY before running the orchestrator."
