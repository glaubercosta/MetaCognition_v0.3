# README - MetaCognition v0.3

## Visao Geral
MetaCognition e o orquestrador de agentes e fluxos do projeto, oferecendo API FastAPI, UI React (Vite) servida pelo backend e, a partir da Sprint 3, migrando para um motor de orquestracao baseado em LangChain + LangGraph. Este README documenta o fluxo operacional alinhado com a decisao do ADR de 27/10/2025 e concentra os links para os demais artefatos oficiais.

## Funcionalidades Principais
- CRUD de agentes e fluxos com contratos Pydantic.
- Importacao/exportacao em JSON ou YAML via `GET/POST /agents|flows`.
- Orquestracao com stubs `robotgreen` e `fake`, e novo engine baseado em LangChain/LangGraph (em desenvolvimento).
- Stub `/evaluations` local enquanto nao ha camada metacognitiva dedicada.
- UI React para gerenciamento e execucao basica.
- Validadores dedicados (`/agents/validate`, `/flows/validate`) e conversor Markdown (`/convert/agent-md`).

## Instalacao
1. Clone o repositorio e crie um ambiente virtual Python 3.11+ se desejar rodar sem Docker.
2. Copie variaveis padrao: `cp .env.example .env`.
3. Construa os containers: `docker compose up --build`.
4. (Opcional) Rode os testes diretamente no host: `pip install -r requirements.txt && pytest -q`.
5. Para usar provedores LangChain adicionais, instale pacotes extras conforme abaixo:
   - OpenAI: `pip install langchain-openai`
   - Google Gemini: `pip install langchain-google-genai`
   - Ollama/self-host: `pip install langchain-community`

## Uso
- API: `http://localhost:8000` (orchestrator) com documentacao interativa em `/docs`.
- UI: `http://localhost:8000/` servindo o build React.
- Engine LangChain (em desenvolvimento): configuracoes documentadas abaixo; stubs permanecem disponiveis durante a migracao.
- Testes: `docker compose run --rm orchestrator pytest -q`.

### Importacao, Validacao e Conversao

- `POST /agents/import` e `POST /flows/import`: aceitam JSON ou YAML (payload direto ou upload `.json/.yaml`). 
- `POST /agents/validate` e `POST /flows/validate`: retornam `{ok, errors[]}` sem persistir dados, úteis para pré-validação no frontend.
- `POST /convert/agent-md`: recebe Markdown com front-matter YAML (`---`) e retorna JSON válido de agente.
- Limites configuráveis:
  - `IMPORT_MAX_FILE_MB` controla o tamanho máximo de upload (0 = sem limite).
  - `IMPORT_MAX_ITEMS` limita a quantidade de registros por requisição (0 = sem limite).
  - `PROMPT_MAX_BYTES` restringe o tamanho dos prompts e é aplicado nos modelos Pydantic (`AgentCreate`).

## Configuracoes Avancadas
- Variaveis principais: `EVAL_MODE` (`off|sync|async`), `METACOG_BASE_URL`, `METACOG_DEFAULT_RUBRIC`.
- Ajuste de limite de importacao via `IMPORT_MAX_FILE_MB`, `IMPORT_MAX_ITEMS`, `PROMPT_MAX_BYTES` (herdado do backlog).
- Logs configurados via `LOG_LEVEL` no `.env`.
- Engine LangChain/LangGraph: configurar provedores suportados pelo LangChain (`LANGCHAIN_MODEL_PROVIDER`, `LANGCHAIN_API_KEY`, variaveis conforme driver escolhido). Exemplos e scripts serao adicionados durante a implementacao.
- Integracao CrewAI real (legado/opcional): `CREWAI_MODE`, `CREWAI_HTTP_MODE`, `CREWAI_API_KEY`, `CREWAI_BASE_URL`, `CREWAI_RUN_PATH`, `CREWAI_MODEL`, `CREWAI_TIMEOUT_SEC`, `CREWAI_MAX_RETRIES`, `CREWAI_BACKOFF_SEC`.

### LangChain Providers
- `stub` (default): nao requer dependencia adicional; retorna respostas deterministicas para desenvolvimento.
- `openai`: requer `pip install langchain-openai` e variaveis `LANGCHAIN_PROVIDER=openai`, `LANGCHAIN_MODEL` (ex.: `gpt-4o-mini`) e `LANGCHAIN_API_KEY` (ou `OPENAI_API_KEY`).
- `google-gemini`: requer `pip install langchain-google-genai` e variaveis `LANGCHAIN_PROVIDER=google-gemini`, `LANGCHAIN_MODEL` (ex.: `gemini-1.5-pro`) e `LANGCHAIN_API_KEY` (ou `GOOGLE_API_KEY`).
- `ollama` (self-host): requer `pip install langchain-community`, `LANGCHAIN_PROVIDER=ollama`, `LANGCHAIN_MODEL` (ex.: `llama3.1`) e servidor Ollama ativo (`LANGCHAIN_BASE_URL`, default `http://localhost:11434`).
- Outros provedores podem ser adicionados conforme necessidade implementando novos factories em `app/integrations/langchain_client.py`.

## Estrutura de Saida
- Agentes/fluxos exportados em JSON ou YAML; cada arquivo inclui metadados (`id`, `name`, `description`, `nodes`).
- Futuro servico metacog retornara `runId`, `artifacts` e `trace` agregados ao `POST /orchestrate/run`.
- Testes geram relatórios padrao pytest na saida do container.

## Arquitetura e Estrutura do Projeto
- `app/`: API FastAPI com routers de agentes, fluxos, orchestrate e testes.
- `frontend/`: UI React (Vite) com componentes e build estatico.
- `orchestration/`: motores (stubs + LangChain/LangGraph em evolucao).
- `data/`: pasta de persistencia SQLite.
- `doc/`: artefatos de documentacao (Project KB, guia de ADR, fluxo de documentacao).

## Solucao de Problemas
- Erros de dependencia: delete `venv/` local e reinstale `pip install -r requirements.txt`.
- Falha ao subir containers: confirmar `.env` e rodar `docker compose down -v && docker compose up --build`.
- Timeout no orchestrator: verificar se `EVAL_MODE` esta em `off` enquanto o metacog nao esta ativo.

## Contribuicao
- Crie branch a partir de `main`, siga TDD e abra PR com descricao clara.
- Atualize `doc/project_kb.md` e registros de ADR quando incluir novas decisoes.
- Executar `pytest -q` e, quando aplicavel, validar JSON Schemas antes do PR.

## Licenca e Suporte
- Licenca: definir (placeholder). Adotar MIT se nenhum outro acordo for estabelecido.
- Contato: squad MetaCognition (Slack interno / e-mail do time).

## Referencias
- Base de conhecimento: `doc/project_kb.md`.
- Roadmap: `ManagementArtifacts/Documentacao/ROADMAP.md`.
- Guia de ADRs: `doc/adr-readme.md`.
