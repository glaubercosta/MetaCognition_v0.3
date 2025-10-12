# Orchestrator & Agent Repository (FastAPI) — TDD-First + UI + Import/Export

Módulo de **orquestração de agentes** com **repositório**, **edição**, **execução de fluxos**, **import/export (YAML/JSON)** e **UI React (CDN)** servida pela própria API.

- **Stack:** Python 3.11, FastAPI, PyTest, SQLite, Docker, docker-compose.
- **TDD:** testes em `app/tests/` (health, agents, orchestrate, io).
- **Orquestração:** interface única + adapters (stub) `CrewAI` e `RobotGreenAI`.
- **UI:** React (CDN, sem build) servida via `StaticFiles`.

---

## 🚀 Como rodar com Docker

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000/docs
- UI:  http://localhost:8000/

---

## 🧪 Testes (TDD)

```bash
docker compose run --rm orchestrator pytest -q
```

Fluxo **Red → Green → Refactor**:
1. Escreva/ajuste um teste em `app/tests/`
2. Rode `pytest` e veja falhar
3. Implemente o mínimo pra passar
4. Refatore mantendo verde

---

## 📡 Endpoints principais

- `GET /health`
- **Agents:** `POST /agents`, `GET /agents`, `GET /agents/{id}`, `PUT /agents/{id}`, `DELETE /agents/{id}`
- **Flows:** `POST /flows`, `GET /flows`, `GET /flows/{id}`
- **Orchestrate:** `POST /orchestrate/run` (engine: `crewai` | `robotgreen`)
- **Evaluations:** `POST /evaluations`, `GET /evaluations`
- **Import/Export:**
  - `GET /agents/export?format=json|yaml` / `POST /agents/import?format=json|yaml`
  - `GET /flows/export?format=json|yaml`  / `POST /flows/import?format=json|yaml`

> Import aceita **array** diretamente ou `{"items":[...]}`. Para YAML, envie corpo como string YAML.

---

## 🖥️ UI React (CDN)

UI simples para:
- listar/criar agentes
- listar/criar fluxos
- executar fluxo (selecionando engine)
- exportar JSON/YAML

Servida pela API (sem build): `GET /`

---

## 🔧 Configuração (Env)

Veja `.env.example`:
- `APP_ENV`, `LOG_LEVEL`
- `DEFAULT_ENGINE` (`crewai` | `robotgreen`)
- `DATABASE_URL` (sqlite em `data/app.db` por padrão)

---

## 🧭 Roadmap

- Integrar adapters com engines reais (CrewAI/RobotGreen)
- UI com build (Vite/React) e editor visual de fluxos
- RBAC, AuthN/AuthZ e audit logs
- Observabilidade (tracing, metrics) e fila assíncrona
