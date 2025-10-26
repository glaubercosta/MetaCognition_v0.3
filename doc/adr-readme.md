# Guia de ADRs - MetaCognition

## Proposito
Documentar decisoes arquiteturais e de produto que impactam o MetaCognition, garantindo rastreabilidade entre contexto de negocio, backlog e implementacoes tecnicas. Os ADRs devem explicar o motivo da escolha e facilitar auditorias futuras.

## Estrutura Padrao
1. **Titulo**: descricao curta.
2. **Status**: Proposto | Aceito | Em revisao | Substituido por `<ADR>` | Rejeitado.
3. **Contexto**: problema, restricoes e metricas.
4. **Decisao**: escolha realizada e justificativa.
5. **Consequencias**: impactos positivos/negativos e riscos residuais.
6. **Relacionados**: links para `doc/project_kb.md`, roadmap, PRs, issues ou documentos relevantes.

## Processo de Gestao
1. Criar ADR como Proposto quando a decisao estiver em discussao (ex: abertura de PR, inicio de sprint).
2. Validar em reuniao tecnica/Produto; registrar participantes e data.
3. Atualizar para Aceito ao finalizar implementacao ou quando a decisao for oficializada.
4. Se a decisao mudar, criar novo ADR, marcar o antigo como Substituido e atualizar referencias cruzadas.
5. Manter ADRs rejeitados para historico, registrando o motivo.

## Operacionalizacao
- Local padrao: `doc/adr/ADR-YYYYMMDD-descricao-curta.md`.
- Manter indice `doc/adr/index.md` ou `doc/adr/README.md` com status e links.
- Atualizar o Project KB (`doc/project_kb.md`) toda vez que um ADR for Aceito ou Substituido.
- Referenciar ADRs relevantes no README (`doc/readme.md`) sempre que houver fluxo novo ou mudanca de setup.

## Convencoes
- Escrever em linguagem direta, destacando o "por que" e as alternativas descartadas.
- Listar riscos residuais e proximos passos decorrentes da decisao.
- Incluir metadados (autor, revisores, data) no topo do ADR.
- Utilizar PRs dedicados por decisao quando possivel, facilitando o diff e a revisao.

## Checklist Rapido
- [ ] Titulo objetivo descrevendo a decisao.
- [ ] Contexto alinha com items do sprint plan ou backlog.
- [ ] Consequencias cobrem impactos tecnicos e de usuario.
- [ ] Relacionados apontam para `doc/project_kb.md`, roadmap ou PR.
- [ ] Status atualizado e sincronizado com os demais documentos.
