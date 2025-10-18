# README (extract)

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
- `DEFAULT_ENGINE` (`crewai` | `robotgreen`)
- `DATABASE_URL` (sqlite em `data/app.db` por padrão)

Integração CrewAI (feature flag):
- `CREWAI_MODE` (`stub` | `real`) — padrão: `stub`.
- `CREWAI_API_KEY` — obrigatório apenas quando `CREWAI_MODE=real`.
- `CREWAI_HTTP_MODE` (`dry-run` | `http`) — padrão: `dry-run`. Em `http`, o adapter usa chamadas HTTP reais do cliente.
- `CREWAI_BASE_URL` (opcional; padrão: `https://api.crewai.example`).
- `CREWAI_RUN_PATH` (opcional; caminho da API; padrão: `/v1/run`).
- `CREWAI_MODEL` (opcional; ex.: `crewai-large`).

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
