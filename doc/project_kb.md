# PROJECT_KB - MetaCognition v0.3

## Cabecalho
- Projeto: MetaCognition
- Data de revisao: 2025-10-26
- Responsavel: Squad MetaCognition
- Gatilho: Planejamento da Sprint 3 (`ManagementArtifacts/Documentacao/SPRINT_3_PLAN.md`) e alinhamento com o resumo executivo de 13/10/2025

## Descricao Geral
MetaCognition entrega um orquestrador de agentes e fluxos com pipeline TDD, importacao/exportacao em JSON/YAML e UI React servida pelo proprio backend FastAPI. Com o cancelamento do ADR do servico metacog, a Sprint 3 passa a focar no MVP funcional de agentes/fluxos, cobrindo contratos, integracoes reais e experiencia de uso final sem metacognicao. Em 26/10 concluimos o pacote de validacao/importacao com limites configuraveis e conversor Markdown -> JSON para agentes; atividades restantes de UX, seguranca e onboarding foram realocadas para a Sprint 4 (`ManagementArtifacts/Documentacao/SPRINT_4_PLAN.md`).

## Status Atual
### Versao vigente
- API FastAPI com CRUD de agentes e fluxos, health check e import/export funcional.
- Endpoints auxiliares `/agents/validate`, `/flows/validate` e `/convert/agent-md` permitem revisar dados antes de persistir.
- UI React (Vite) publicada estaticamente via `GET /`.
- Limites configuraveis (`IMPORT_MAX_FILE_MB`, `IMPORT_MAX_ITEMS`, `PROMPT_MAX_BYTES`) aplicados via `app/config.py` e utilizados nos validadores.
- Tela de Import/Export atualizada com validacao inline, upload JSON/YAML e conversao Markdown -> JSON.
- Adapters stubs para engines `crewai`, `robotgreen` e `fake`, cobertos por testes.
- Endpoint `/orchestrate/run` aciona adapters existentes e gera artefatos padrao.
- Stub `/evaluations` interno com SQLite garante compatibilidade temporaria enquanto o metacog nao entra em operacao.

### Limitacoes
- Processo de avaliacao ainda depende do stub local; integracao real com o servico metacog esta em construcao.
- Persistencia primaria em SQLite; migracao para PostgreSQL permanece no roadmap, sem datas definidas.
- Testes de contrato para os novos JSON Schemas ainda nao estao integrados ao CI (execucao manual via `pytest`).
- UI de edicao ainda nao entrega preview Markdown unificado; parte da Story 4 permanece aberta.
- Sem recursos de metacognicao; avaliacao avancada foi postergada para iteracoes futuras.

### Fluxos operacionais em uso
- Desenvolvimento local: `cp .env.example .env` seguido de `docker compose up --build`.
- Execucao de testes: `docker compose run --rm orchestrator pytest -q` (ou `PYTHONPATH=. pytest` fora do container).
- Importacao e exportacao de artefatos via `GET/POST /agents|flows` com query `format=json|yaml` ou upload multipart (JSON/YAML) com validacao automatica.
- Conversao de agentes Markdown -> JSON via `POST /convert/agent-md` ou tela de Import/Export.

## Proximas Etapas
### Curto prazo (Sprint 3 - ate 2025-10-27)
- Formalizar contratos de engines/adapters e publicar JSON Schemas no CI. **Status:** concluido.
- Implementar engine LangChain/LangGraph com fluxo real e testes de integracao. **Status:** concluido.
- Expandir import/validate (limites configuraveis, endpoints auxiliares, convert). **Status:** concluido em 26/10 (backend + frontend + testes automatizados).
- Evoluir UI de edicao (Markdown + formulario) e publicar exemplos oficiais. **Status:** parcialmente concluido; editor/preview movidos para Sprint 4.
- Revisar seguranca basica, sanitizacao e pipelines CI/E2E. **Status:** reprogramado para Sprint 4.
- Atualizar documentacao e guia de onboarding para usuarios finais. **Status:** em andamento; entregaveis finais migrados para Sprint 4.

### Medio prazo (6-8 semanas)
- Ligar adapters reais de engines sob feature flags e reforcar hardening de import/export.
- Introduzir observabilidade compartilhada (tracing, logs, metricas) entre orchestrator e metacog.
- Evoluir seguranca com RBAC/Auth e auditoria basica.

### Longo prazo (9-12 semanas)
- Disponibilizar fila assincrona para avaliacao (`async`) e editor visual de fluxos.
- Publicar biblioteca de exemplos, guias de contribuicao e hardening DevSecOps (SAST/DAST, SBOM).
- Preparar terreno para migracao de persistencia (PostgreSQL) e release candidate.

## Premissas Tecnicas
- Linguagem principal: Python 3.11; framework FastAPI.
- UI: React + Vite com build estatico.
- Persistencia atual: SQLite em `data/app.db`; eventual storage dedicado ao metacog permanece em estudo.
- Empacotamento: Docker + docker-compose com container principal do orquestrador; container `metacog` segue opcional e condicionado a nova aprovacao.
- Testes: pytest com enfoque TDD; validacao de JSON Schemas programada para o CI.
- Feature flag `EVAL_MODE` controla ligacao com o metacog (`off`, `sync`, `async`).
- LangChainEngine suporta provedores stub, OpenAI, Google Gemini e Ollama; pacotes opcionais devem ser instalados conforme necessidade.
- CrewAI real permanece como opcional legado via feature flags (`CREWAI_MODE`, `CREWAI_HTTP_MODE`) e configuracoes de resiliencia (`CREWAI_TIMEOUT_SEC`, `CREWAI_MAX_RETRIES`, `CREWAI_BACKOFF_SEC`).

## Retroalimentacao Continua
- Revisar este KB ao final de cada sprint ou PR relevante que altere escopo, stack ou fluxos operacionais.
- Concilia-lo com as atualizacoes do README operacional e com os ADRs aceitos.
- Registrar os principais deltas em changelog ou comunicacao de rollout apos cada sincronizacao.

## Decisoes Importantes
- Proposta de separar a camada metacog como servico dedicado foi rejeitada (`doc/adr/ADR-20251027-metacog-service.md`); metacognicao fica fora do MVP.
- Adocao de LangChain + LangGraph como motor de orquestracao para substituir o caminho CrewAI SaaS (`doc/adr/ADR-20251027-langchain-orchestration.md`, status Aceito).
- Manter avaliacao basica no orquestrador ate nova revisao arquitetural.
- Estrategia Docker-first para desenvolvimento e troca de ambientes (ADR em elaboracao; manter item como risco ate formalizacao).

## Operacao e Metricas
- Monitorar tempo de resposta do orchestrator e do futuro servico metacog para garantir viabilidade dos modos `sync` e `async`.
- Acompanhar volume de agentes/fluxos importados para validar limites de payload.
- Registrar execucoes com `runId`, `artifacts` e `trace` para preparar telemetria e auditoria.

## Seguranca e Privacidade
- Manter chaves e configuracoes sensiveis em variaveis de ambiente; nunca commitar `.env`.
- Planejar integracao com RBAC/Auth antes de abrir endpoints de avaliacao para consumo externo.
- Avaliar sanitizacao de dados trafegados para metacog, especialmente quando envolver feedback de modelos externos.

## Anexos e Referencias
- Planejamento atual: `ManagementArtifacts/Documentacao/SPRINT_3_PLAN.md`.
- Proximo ciclo: `ManagementArtifacts/Documentacao/SPRINT_4_PLAN.md`.
- Resumo executivo vigente: `ManagementArtifacts/Documentacao/EXECUTIVE_SUMMARY.md`.
- Roadmap alinhado: `ManagementArtifacts/Documentacao/ROADMAP.md`.
- Guia de ADRs: `doc/adr-readme.md`.
- README operacional: `doc/readme.md`.






