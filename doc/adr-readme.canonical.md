# Guia de ADRs - Versao Canonica

## Proposito
Estabelecer uma referencia oficial para criacao, manutencao e auditoria de Architecture Decision Records (ADRs) no projeto AnalistaDeDados, garantindo rastreabilidade entre decisoes, contexto de negocio e implementacoes tecnicas.

## Estrutura Padrao de um ADR
1. **Titulo**: frase curta e descritiva.
2. **Status**: Proposto | Aceito | Em Revisao | Substituido por `<ADR>` | Rejeitado.
3. **Contexto**: problema, restricoes e metricas relevantes.
4. **Decisao**: escolha realizada e justificativa.
5. **Consequencias**: impactos positivos, negativos e riscos residuais.
6. **Relacionados**: links para KB, roadmap, prompts afetados, issues e PRs.

## Processo de Gestao
1. Registrar ADR como Proposto quando a decisao ainda esta em discussao.
2. Revisar em conjunto com time tecnico e produto; documentar participantes e data.
3. Atualizar para Aceito assim que a decisao for adotada; registrar tarefas derivadas.
4. Quando uma decisao for alterada, criar novo ADR, marcar o antigo como Substituido por `<ADR>` e atualizar referencias cruzadas.
5. Arquivar ADRs rejeitados mantendo justificativa para auditoria futura.

## Operacionalizacao
- Nomear arquivos seguindo `ADR-YYYYMMDD-descricao-curta.md`.
- A cada ciclo de sincronizacao (vide KB Sync Agent), verificar se houve mudancas de contexto que exijam revisao dos ADRs.
- Referenciar ADRs relevantes em `docs/prompts.md`, `docs/PROJECT_KB.md` e `docs/roadmap.md`.
- Manter indice em `docs/adr/index.json` ou `README.md` com lista ordenada por data e status.

## Boas Praticas
- Escrever em linguagem clara, focando no "por que" da decisao.
- Citar alternativas consideradas e riscos que permanecem.
- Incluir metadados (autor, revisores, data de revisao).
- Utilizar PRs dedicados para cada ADR quando possivel, facilitando auditoria.

