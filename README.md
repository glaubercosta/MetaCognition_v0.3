


## Configuração (Env)

Veja .env.example:
- APP_ENV, LOG_LEVEL
- DEFAULT_ENGINE (crewai | obotgreen)
- DATABASE_URL (sqlite em data/app.db por padrão)

Integração CrewAI (feature flag):
- CREWAI_MODE (stub | eal) — padrão: stub.
- CREWAI_API_KEY — obrigatório apenas quando CREWAI_MODE=real.

Exemplos
- PowerShell (ativar modo real dry‑run do CrewAI):
  `powershell
   = 'real'
   = 'minha-chave'
  uvicorn app.main:app --reload --port 8000
  `
- Docker Compose (adicionar ao serviço orchestrator):
  `yaml
  services:
    orchestrator:
      environment:
        CREWAI_MODE: real
        CREWAI_API_KEY: 
  `

---

## Configuração (Env)

Veja .env.example:
- APP_ENV, LOG_LEVEL
- DEFAULT_ENGINE (crewai | obotgreen)
- DATABASE_URL (sqlite em data/app.db por padrão)

Integração CrewAI (feature flag):
- CREWAI_MODE (stub | eal) — padrão: stub.
- CREWAI_API_KEY — obrigatório apenas quando CREWAI_MODE=real.
- CREWAI_HTTP_MODE (dry-run | http) — padrão: dry-run. Em http, o adapter usa chamadas HTTP reais do cliente.

Exemplos
- PowerShell (ativar modo real dry‑run do CrewAI):
  `powershell
   = 'real'
   = 'minha-chave'
  uvicorn app.main:app --reload --port 8000
  `
- PowerShell (ativar modo real com HTTP real, requer backend disponível):
  `powershell
   = 'real'
   = 'minha-chave'
   = 'http'
  uvicorn app.main:app --reload --port 8000
  `
- Docker Compose (adicionar ao serviço orchestrator):
  `yaml
  services:
    orchestrator:
      environment:
        CREWAI_MODE: real
        CREWAI_API_KEY: 
        # CREWAI_HTTP_MODE: http   # opcional
  `
