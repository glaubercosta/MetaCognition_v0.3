# Code Review Plan — Sprint 3 (27/10/2025)

## 1. Escopo
- Backend FastAPI: limites configuráveis (`IMPORT_MAX_FILE_MB`, `IMPORT_MAX_ITEMS`, `PROMPT_MAX_BYTES`), novos utilitários de importação/validação e rota `/convert/agent-md`.
- Modelos Pydantic: validações adicionais para agentes e fluxos (nome/prompt e `graph_json`).
- Endpoints `/agents/validate` e `/flows/validate`, bem como importações reescritas com tratamento de arquivos e erros.
- Frontend (React/Vite): atualizações da tela Import/Export (validação, feedback, conversão Markdown), ajustes na API client (`frontend/src/lib/api.ts`) e na página Orchestration.
- Testes automatizados (`app/tests/test_import_validation.py`) cobrindo limites, validação e conversão.
- Documentação atualizada (`README.md`, `doc/readme.md`, `doc/project_kb.md`, `SPRINT_3_PLAN.md`, `SPRINT_4_PLAN.md`, `ROADMAP.md`) refletindo novas capacidades e replanejamento.
- JSON Schemas de contrato revisados em `ProjectArtifacts/schemas/*`.

## 2. Itens realizados na sprint
1. **Limites configuráveis**: Funções em `app/config.py`, uso nos validadores Pydantic e nos utilitários de importação.
2. **Reestruturação de import/validate**: novos módulos `app/routers/io_support.py` e ajustes em `agents_io.py` / `flows_io.py` para normalização, leitura de payload (JSON/YAML, upload) e mensagens de erro claras.
3. **Conversão Markdown → Agent JSON**: rota `/convert/agent-md` e suporte correspondente no frontend.
4. **Validações adicionais de modelos**: nome obrigatório e limite de prompt para agentes; validação de `graph_json` (nodes/edges) em fluxos.
5. **Front-end Import/Export**: validação antes de import, carregamento de arquivos, alertas de erro/sucesso, integração com endpoints de validação e conversão.
6. **Ajustes na Orchestration UI**: tipagem forte, parse seguro de JSON de logs/inputs.
7. **Atualização das APIs TypeScript**: tratamento de erros normalizado, tipos explícitos para resultados de import/validate.
8. **Cobertura de testes**: novo módulo `test_import_validation.py` e execução local (`PYTHONPATH=. pytest`).
9. **Documentação e roadmap**: alinhamento de README, KB, plano da sprint e novo plano para o próximo ciclo.

## 3. Critérios de aceitação para aprovação do review
- **Conformidade funcional**:
  - Limites configuráveis respeitados em importação/validação e prompts de agentes.
  - Endpoints `/agents/validate`, `/flows/validate`, `/convert/agent-md` respondem conforme esperado (códigos HTTP e payloads coerentes).
  - Frontend Import/Export exibe feedback correto, recusa payloads inválidos e executa conversão Markdown → JSON.
- **Qualidade técnica**:
  - Validações Pydantic cobrem cenários descritos; erros retornam mensagens claras.
  - Reutilização dos utilitários `io_support` nos routers evita duplicação e mantém consistência.
  - Tipagens TypeScript atualizadas (sem `any` residual) e lint (`npm run lint`) executa sem erros.
  - JSON Schemas em `ProjectArtifacts/schemas` alinham com modelos atuais (diferenças examinadas).
- **Testes**:
  - `PYTHONPATH=. pytest` passa (30 testes, 1 warning conhecido do httpx).
  - Opcional: `npm run lint` (frontend) executado; warnings existentes documentados (react-refresh).
- **Documentação**:
  - README, `doc/readme.md`, KB e planos de sprint refletem novas rotas, limites e próximos passos.
  - Novos endpoints/variáveis constam em `.env.example` e `.env`.
- **Observações de revisão**:
  - Avaliar impacto nas rotas existentes e compatibilidade com dados anteriores.
  - Confirmar ausência de regressões em importação/exportação (JSON e YAML) com dados reais.
