# ADR-20251027-langchain-orchestration - Adotar LangChain + LangGraph como motor de orquestracao

- **Data**: 2025-10-27
- **Status**: Aceito
- **Autor**: Squad MetaCognition
- **Revisores**: Glauber Costa
- **Ligacoes**: `doc/project_kb.md`, `ManagementArtifacts/Documentacao/SPRINT_3_PLAN.md`, `ManagementArtifacts/Documentacao/ROADMAP.md`

## Contexto

- O projeto vinha utilizando o adapter `CrewAI` como caminho principal para execucao real de fluxos multiagentes.
- A integracao oficial depende da API SaaS do fornecedor, sujeita a custos recorrentes, limites de uso e negociacoes contratuais ainda nao concluídas.
- Em paralelo, a equipe levantou alternativas open source (LangChain + LangGraph, Haystack, Autogen) e identificou que `CrewAI` nao possui opcao self-host gratuita que replique o endpoint esperado pelo orquestrador.
- O roadmap do MVP prioriza manter todo o pipeline em Python/FastAPI, com forte cobertura de testes automatizados e independencia de servicos proprietarios quando possivel.
- Ja existem stubs locais (Fake, RobotGreen) e novos contratos em `ProjectArtifacts/schemas/` que podem ser reutilizados por um engine Python puro.

## Decisao

Adotar **LangChain** em conjunto com **LangGraph** como base oficial do novo motor de orquestracao de agentes e fluxos. O plano contempla:
- Implementar uma camada `LangChainEngine`/`LangGraphEngine` que mapeie cada no do flow para uma chain/graph correspondente, reaproveitando o contrato `OrchestrationResult`.
- Descontinuar a dependencia do `CrewAI` SaaS no MVP; o adapter atual fica preservado apenas como opcional ate a migracao completa, com feature flag default `stub`.
- Manter suporte aos stubs existentes (Fake, RobotGreen) para testes rapidos, mas alinhar toda a evolucao funcional com LangChain/LangGraph.
- Suportar tanto modelos SaaS (OpenAI, etc.) quanto modelos self-hosted, liberando integracoes futuras sem travar a arquitetura.

## Consequencias
### Positivas

- Remove dependencia direta de um fornecedor SaaS e elimina custo recorrente para o MVP.
- Mantem o orquestrador 100% em Python, facilitando testes, observabilidade e extensoes.
- Ecossistema vasto: LangChain e LangGraph oferecem conectores, memoria, ferramentas de RAG e workflows declarativos compatíveis com a visao do projeto.
- Permite evoluir gradualmente, migrando fluxos do CrewAI para LangChain sem reescrever o backend ou UI.

### Negativas / Riscos

- Trabalho adicional para implementar e estabilizar o engine baseado em LangChain/LangGraph, incluindo traducao de flows atuais.
- Curva de aprendizado: a equipe precisa dominar APIs do LangGraph para definir grafos de execucao e garantir comportamento deterministico.
- Necessidade de provisionar modelos (SaaS ou open source) para uso real; sem isso, o engine entrega apenas mocks.
- Ajustes em testes e documentacao podem consumir parte da sprint e exigir revisao dos contratos de logs/telemetria.

### Mitigacoes

- Planejar entregas incrementais (ex.: primeiro suporte a um fluxo sequencial simples, depois ramos/condicionais).
- Manter os adapters Fake/RobotGreen como fallback imediato ate que LangChain esteja validado.
- Aproveitar a infraestrutura de JSON Schemas e contratos existentes para validar o novo engine em CI.
- Atualizar documentacao (README, Project KB, onboarding) com exemplos de configuracao e operacao do LangChainEngine.

## Relacionados

- Avaliacoes anteriores sobre CrewAI e self-host (`doc/adr/ADR-20251027-metacog-service.md` - indeferido).
- `doc/project_kb.md`: prox etapas da Sprint 3 e estrategia do MVP.
- `ManagementArtifacts/Documentacao/SPRINT_3_PLAN.md`: checklist e historias focadas em agentes/fluxos.
