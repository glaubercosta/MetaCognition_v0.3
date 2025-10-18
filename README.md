# Orchestrator & Agent Repository (FastAPI) — TDD-First + UI + Import/Export

Módulo de orquestração de agentes com repositório, edição, execução de fluxos, import/export (YAML/JSON) e UI React (Vite) servida pela própria API.

- Stack: Python 3.11, FastAPI, PyTest, SQLite, Docker, docker-compose.
- TDD: testes em `app/tests/` (health, agents, orchestrate, io).
- Orquestração: interface única + adapters (stub) `CrewAI` e `RobotGreenAI`.
- UI: React + Vite (TypeScript + shadcn/ui) em `frontend/`, servida via build estático em `public/`.

Links
- Changelog: `CHANGELOG.md`
- Guia de integração (resumo): `ProjectArtifacts/frontend_docs/INTEGRATION_NOTES.txt`
- Guia detalhado: `ProjectArtifacts/frontend_docs/INTEGRACAO_DESIGN.md`

---

## Como rodar com Docker

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000/docs
- UI:  http://localhost:8000/

Notas
- Em desenvolvimento, o compose monta `.:/app`. O conteúdo local de `public/` é servido pela API.
- A imagem Docker (multi-stage) já embute o build do frontend em `/app/public/`.

---

## Como construir a UI (Vite)

Opção 1 (Makefile):
```bash
make frontend-all
```

Opção 2 (manual):
```bash
cd frontend
npm ci || npm install
npm run build
cd ..
PowerShell: Copy-Item -Path "frontend/dist/*" -Destination "public/" -Recurse -Force
# ou Linux/Mac: cp -r frontend/dist/* public/
```

A API serve automaticamente `./public` quando existe `index.html` (fallback para `./ui/public`).

---

## Executar localmente (sem Docker)

Pré‑requisitos: Python 3.11 e Node (para build opcional da UI).

Backend
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# ou no Windows PowerShell:
# .\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend (opcional, apenas se precisar rebuildar a UI)
```bash
cd frontend
npm ci || npm install
npm run build
cd ..
cp -r frontend/dist/* public/   # PowerShell: Copy-Item -Path "frontend/dist/*" -Destination "public/" -Recurse -Force
```

Parar o servidor local
- Ctrl+C no terminal onde o `uvicorn` está rodando.
- Se necessário encerrar por porta (Windows): `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force`

---

## Testes (TDD)

```bash
docker compose run --rm orchestrator pytest -q
```

Executar testes localmente (sem Docker):
- PowerShell (Windows):
  ```powershell
  $env:PYTHONPATH = (Get-Location).Path; pytest -q
  ```
- Linux/Mac:
  ```bash
  PYTHONPATH=$(pwd) pytest -q
  ```

Cobertura (local ou em CI):
```bash
pytest -q --cov=app --cov-report=term-missing
```

Fluxo Red → Green → Refactor:
1. Escreva/ajuste um teste em `app/tests/`
2. Rode `pytest` e veja falhar
3. Implemente o mínimo para passar
4. Refatore mantendo verde

---

## Endpoints principais

- `GET /health`
- Agents: `POST /agents`, `GET /agents`, `GET /agents/{id}`, `PUT /agents/{id}`, `DELETE /agents/{id}`
- Flows: `POST /flows`, `GET /flows`, `GET /flows/{id}`
- Orchestrate: `POST /orchestrate/run` (engine: `crewai` | `robotgreen`)
- Evaluations: `POST /evaluations`, `GET /evaluations`
- Import/Export:
  - `GET /agents/export?format=json|yaml` / `POST /agents/import?format=json|yaml`
  - `GET /flows/export?format=json|yaml`  / `POST /flows/import?format=json|yaml`

> Import aceita array diretamente ou `{ "items": [...] }`. Para YAML, envie corpo como string YAML.

---

## UI React (Vite)

UI moderna para:
- listar/criar/editar/excluir agentes
- listar/criar fluxos e executar orquestrações (engine)
- importar/exportar JSON/YAML

Servida pela API (build estático): `GET /`

---

## Configuração (Env)

Veja `.env.example`:
- `APP_ENV`, `LOG_LEVEL`
- `DEFAULT_ENGINE` (`crewai` | `robotgreen`)
- `DATABASE_URL` (sqlite em `data/app.db` por padrão)

---

## Roadmap

- Integrar adapters com engines reais (CrewAI/RobotGreen)
- Editor visual de fluxos (drag & drop)
- RBAC, AuthN/AuthZ e audit logs
- Observabilidade (tracing, metrics) e fila assíncrona
