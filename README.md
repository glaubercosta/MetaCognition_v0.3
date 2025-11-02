# README Rapido

## Documentacao Complementar
- Guia operacional detalhado: `doc/readme.md`
- Base de conhecimento da sprint: `doc/project_kb.md`
- Decisoes arquiteturais: `doc/adr/index.md`
- Esquemas JSON oficiais: `ProjectArtifacts/schemas/`

## Politica de Build (UI)

- Durante o desenvolvimento, o bundle React e gerado em `frontend/` e copiado para `public/`.
- Apenas arquivos estaticos base (por exemplo `index.html`, `favicon.ico`, `robots.txt`, `placeholder.svg`) permanecem versionados.
- A pasta `public/assets/` deve ficar vazia no git (somente `.gitkeep`). Arquivos gerados com hash nao podem ser commitados.
- O alvo `make frontend-all` instala dependencias, executa `npm run build`, limpa `public/assets/` e copia o resultado.
- O job `hygiene` do CI valida essa politica e tambem bloqueia commits com blobs grandes.
- Em releases, o build continua empacotado via multi-stage no Dockerfile ou disponibilizado como artefato fora da branch principal.

### Comandos uteis
- `make frontend-all` – instala dependencias, gera o build e publica em `public/`.
- `make deploy-frontend` – apenas copia `frontend/dist` para `public/` apos o build local.

#### Build frontend (Windows)
Se estiver em Windows e sem `make` instalado, use o helper PowerShell que automatiza install/build/copy:

```powershell
# executar a partir da raiz do projeto
.\scripts\frontend-build.ps1
```

Esse script vai executar `npm ci`/`npm install` quando necessário, `npm run build` em `frontend/` e copiar o conteúdo de `frontend/dist/` para `public/`.

## Configuracao (.env)

Veja `.env.example` para valores base:
- `APP_ENV`, `LOG_LEVEL`
- `DEFAULT_ENGINE` (`langchain` | `robotgreen` | `fake` | `crewai`)
- `DATABASE_URL` (por padrao `sqlite:///data/app.db`)
- Limites de importacao:
  - `IMPORT_MAX_FILE_MB` – tamanho maximo (MB) aceito em uploads; `0` desabilita a verificacao.
  - `IMPORT_MAX_ITEMS` – quantidade maxima de registros por carga; `0` desabilita.
  - `PROMPT_MAX_BYTES` – limite em bytes para prompts de agentes; aplicado nos validadores Pydantic.

### Engine LangChain/LangGraph
- Variaveis especificas do provedor (`LANGCHAIN_PROVIDER`, `LANGCHAIN_MODEL`, `LANGCHAIN_API_KEY`, etc.) sao mapeadas conforme o conector.
- Provedores pronto-uso:
  - `stub` (default) – sem dependencias extras; respostas deterministicas.
  - `openai` – instale `pip install langchain-openai`; defina `LANGCHAIN_MODEL` (ex.: `gpt-4o-mini`) e `LANGCHAIN_API_KEY` (ou `OPENAI_API_KEY`).
  - `google-gemini` – instale `pip install langchain-google-genai`; defina `LANGCHAIN_MODEL` (ex.: `gemini-1.5-pro`) e `LANGCHAIN_API_KEY` (ou `GOOGLE_API_KEY`).
  - `ollama` – instale `pip install langchain-community`; defina `LANGCHAIN_MODEL` (ex.: `llama3.1`) e mantenha servidor Ollama em `LANGCHAIN_BASE_URL` (default `http://localhost:11434`).
- Para outros provedores, estenda `app/integrations/langchain_client.py`.

### Integracao CrewAI (legado/opcional)
- `CREWAI_MODE` (`stub` | `real`) – default `stub`.
- `CREWAI_HTTP_MODE` (`dry-run` | `http`) – default `dry-run`; em `http` ocorrem chamadas reais.
- `CREWAI_API_KEY`, `CREWAI_BASE_URL`, `CREWAI_RUN_PATH`, `CREWAI_MODEL`, `CREWAI_TIMEOUT_SEC`, `CREWAI_MAX_RETRIES`, `CREWAI_BACKOFF_SEC` – configuracoes opcionais utilizadas apenas quando `CREWAI_MODE=real`.

### Exemplos rapidos
- PowerShell (ativar CrewAI dry-run):
  ```powershell
  $env:CREWAI_MODE = 'real'
  $env:CREWAI_API_KEY = 'minha-chave'
  uvicorn app.main:app --reload --port 8000
  ```
- Docker Compose:
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
