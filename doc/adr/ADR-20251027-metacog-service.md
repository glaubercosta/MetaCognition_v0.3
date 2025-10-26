# ADR-20251027-metacog-service - Separar o servico de avaliacao (metacog) como componente dedicado

- **Data**: 2025-10-27
- **Status**: Indeferido
- **Autor**: Squad MetaCognition
- **Revisores**: Glauber Costa
- **Ligacoes**: `doc/project_kb.md`, `ManagementArtifacts/Documentacao/SPRINT_3_PLAN.md`, `ManagementArtifacts/Documentacao/ROADMAP.md`

## Contexto
- O orquestrador MetaCognition v0.3 fornece `/orchestrate/run` com avaliacao acoplada a um stub SQLite exposto via `/evaluations`.
- A Sprint 3 exige habilitar modos `eval=off|sync|async`, gerar `runId` e `artifacts` e acionar um servico especializado.
- O roadmap define a criacao do modulo metacog (FastAPI + Docker) para suportar avaliacao sincronizada/assincrona, versionamento de rubricas e contratos HTTP/JSON.
- Mantendo avaliacao dentro do orquestrador, os testes ficam acoplados, o ciclo de deploy fica mais lento e a evolucao de rubricas/armazenamento exige migracoes na mesma base de dados.

## Decisao
Separar o servico de avaliacao em um componente dedicado (`metacog/`), empacotado como container proprio no docker-compose, responsavel por:
- Expor rotas `/evaluations` (sync/async) e `/rubrics`.
- Persistir dados em storage isolado.
- Validar contratos via JSON Schemas versionados.
- Ser acionado pelo orquestrador apenas quando `EVAL_MODE` estiver em `sync` ou `async`.

O endpoint `/evaluations` existente no orquestrador permanece apenas como compatibilidade durante o periodo de migracao, com plano de sunset definido no backlog da Sprint 3.

## Consequencias
### Positivas
- Reduz acoplamento entre orquestrador e avaliacao, habilitando evolucao independente e escalabilidade dedicada.
- Permite testes de contrato especificos e pipelines de deploy focados na camada metacognitiva.
- Facilita o desenvolvimento de modos `async` com fila/worker sem impactar o orquestrador principal.

### Negativas / Riscos
- Aumenta a complexidade operacional (mais um container, configuracoes `METACOG_BASE_URL`, `METACOG_DEFAULT_RUBRIC`).
- Latencia adicional nas chamadas HTTP pode afetar tempo de execucao ate que metricas e tuning sejam estabelecidos.
- Necessidade de observabilidade e monitoramento adicionais para coordenar falhas entre servicos.

### Mitigacoes
- Manter `EVAL_MODE=off` como fallback enquanto o metacog nao estiver disponivel.
- Adicionar testes de contrato automatizados e validacao de JSON Schemas no CI.
- Documentar setup e troubleshooting no README (`doc/readme.md`) e sincronizar status no Project KB.

## Relacionados
- `doc/project_kb.md`: status atual e proximas etapas da Sprint 3.
- `ManagementArtifacts/Documentacao/SPRINT_3_PLAN.md`: detalhes das tarefas e checklist da sprint.
- `ManagementArtifacts/Documentacao/ROADMAP.md`: marco M3 e horizontes de entrega associados ao servico metacog.

## Justificativa

- A alteracao deste aspecto agora resultaria em um trabalho adicional que nao agrega muito ao MVP além de criar um atraso em sua entrega. Caso futuramente, após a entrega do MVP, o time entender que a mudança se justifica, pode-se voltar ao assunto porém a decisao atual e de indeferir a modificacao.

