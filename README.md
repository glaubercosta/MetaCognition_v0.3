# README (extract)

## Documentacao Complementar
- Guia operacional detalhado: `doc/readme.md`
- Base de conhecimento da sprint: `doc/project_kb.md`
- Decisoes arquiteturais e status: `doc/adr/index.md`
- Esquemas JSON oficiais de contratos: `ProjectArtifacts/schemas/`

## Política de Build (UI)

- Em desenvolvimento, a UI é construída localmente em `frontend/` e os artefatos são copiados para `public/`.
- Artefatos de build não são versionados (pasta `public/assets/` está no `.gitignore`).
- A API serve automaticamente `./public` quando existe `index.html` (fallback para `./ui/public`).
- Em release, o build pode ser:
  - incorporado na imagem Docker via multi-stage (Dockerfile já faz isso), ou
  - publicado como artefato em uma pipeline de release (fora da branch principal).

Makefile/Comandos úteis (dev):
- `make frontend-all` (ou `cd frontend && npm ci && npm run build` e copiar para `public/`).

## Configuração (Env)

Veja `.env.example`:
- `APP_ENV`, `LOG_LEVEL`
- `DEFAULT_ENGINE` (`langchain` | `robotgreen` | `fake` | `crewai`*)
- `DATABASE_URL` (sqlite em `data/app.db` por padrão)

Engine LangChain/LangGraph:
- Variáveis específicas do provedor de LLM escolhido (`LANGCHAIN_PROVIDER`, `LANGCHAIN_MODEL`, `LANGCHAIN_API_KEY`, etc.) são mapeadas conforme o conector.
- Provedores suportados out-of-the-box:
  - `stub` (default) — sem dependências extras; respostas determinísticas para desenvolvimento.
  - `openai` — instale `pip install langchain-openai`; defina `LANGCHAIN_MODEL` (ex. `gpt-4o-mini`) e `LANGCHAIN_API_KEY` (ou `OPENAI_API_KEY`).
  - `google-gemini` — instale `pip install langchain-google-genai`; defina `LANGCHAIN_MODEL` (ex. `gemini-1.5-pro`) e `LANGCHAIN_API_KEY` (ou `GOOGLE_API_KEY`).
  - `ollama` — instale `pip install langchain-community`; defina `LANGCHAIN_MODEL` (ex. `llama3.1`) e mantenha servidor Ollama (`LANGCHAIN_BASE_URL`, default `http://localhost:11434`).
- Para outros provedores, estenda `app/integrations/langchain_client.py` com novo factory.

Integração CrewAI (legado/opcional):
- `CREWAI_MODE` (`stub` | `real`) — padrão: `stub`.
- `CREWAI_API_KEY` — obrigatório apenas quando `CREWAI_MODE=real`.
- `CREWAI_HTTP_MODE` (`dry-run` | `http`) - padrão: `dry-run`. Em `http`, o adapter usa chamadas HTTP reais do cliente.
- `CREWAI_BASE_URL` (opcional; padrão: `https://api.crewai.example`).
- `CREWAI_RUN_PATH` (opcional; caminho da API; padrão: `/v1/run`).
- `CREWAI_MODEL` (opcional; ex.: `crewai-large`).
- `CREWAI_TIMEOUT_SEC` (opcional; tempo de espera por chamada HTTP; padrão: `30`).
- `CREWAI_MAX_RETRIES` (opcional; total de tentativas antes de falhar; padrão: `2`).
- `CREWAI_BACKOFF_SEC` (opcional; incremento do intervalo entre tentativas; padrão: `0.5`).

\* `crewai` permanece disponível apenas como fallback enquanto o engine LangChain/LangGraph é finalizado.

Exemplos
- PowerShell (ativar modo real dry‑run do CrewAI):
  ```powershell
  $env:CREWAI_MODE = 'real'
  $env:CREWAI_API_KEY = 'minha-chave'
  uvicorn app.main:app --reload --port 8000
  ```
- PowerShell (ativar modo real com HTTP real, requer backend disponível):
  ```powershell
  $env:CREWAI_MODE = 'real'
  $env:CREWAI_API_KEY = 'minha-chave'
  $env:CREWAI_HTTP_MODE = 'http'
  $env:CREWAI_BASE_URL = 'https://api.seu-crewai'
  $env:CREWAI_RUN_PATH = '/v1/run'
  uvicorn app.main:app --reload --port 8000
  ```
- Docker Compose (adicionar ao serviço `orchestrator`):
  ```yaml
  services:
    orchestrator:
      environment:
        CREWAI_MODE: real
        CREWAI_API_KEY: ${CREWAI_API_KEY}
        # CREWAI_HTTP_MODE: http
        # CREWAI_BASE_URL: https://api.seu-crewai
        # CREWAI_RUN_PATH: /v1/run
        # CREWAI_MODEL: crewai-large
  ```
