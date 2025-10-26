# PROJECT_KB - Versao Canonica

## Proposito
Manter a base de conhecimento como fonte unica e atualizada do estado do projeto AnalistaDeDados, descrevendo contexto, backlog resumido, premissas tecnicas e integracao com demais artefatos (ADRs, Roadmap, Prompts).

## Estrutura Recomendada
1. **Cabecalho**: identificacao do projeto, data de revisao, responsavel e link do evento (PR/issue/release) que motivou a atualizacao.
2. **Descricao Geral**: objetivo, problema resolvido, stakeholders e limites de escopo.
3. **Status Atual**: versao vigente, funcionalidades entregues, limitacoes e fluxos operacionais em uso.
4. **Proximas Etapas**: backlog resumido com horizonte curto, medio e longo prazo.
5. **Premissas Tecnicas**: qualidade, documentacao, stack, arquitetura e governanca de prompts.
6. **Retroalimentacao Continua**: checkpoints e rotinas de revisao apos cada incremento.
7. **Decisoes Importantes**: indice enxuto de ADRs e marcos adotados.
8. **Operacao e Metricas**: visao geral de monitoramento, persistencia e retencao de dados.
9. **Seguranca e Privacidade**: politicas de chaves, dados sensiveis e limpeza de artefatos.
10. **Anexo Opcional**: referencias cruzadas e links para documentos dedicados.

## Politica de Atualizacao
1. Acionar este documento ao final de cada incremento relevante (merge significativo, release, mudanca de premissa).
2. Atualizar secoes 2-4 com fatos mais recentes; mover itens entregues do backlog para Status Atual.
3. Registrar novas decisoes e linkar para ADR correspondente; quando ADR for substituido, atualizar indice imediatamente.
4. Sincronizar referencias com `docs/prompts.md` e `docs/roadmap.md` no mesmo ciclo.
5. Manter historico curto (1-2 paginas). Detalhes adicionais devem migrar para ADRs, roadmap ou anexos dedicados.

## Checklist Antes de Concluir Revisao
- Confirmar que premissas tecnicas refletem stack atual e limites de tokens.
- Validar que as entradas do backlog estao alinhadas com roadmap vigente.
- Garantir que fluxos operacionais descritos cobrem UI, CLI e quaisquer pipelines novos.
- Revisar links e artefatos citados (ADRs, prompts, scripts) para evitar referencias quebradas.

## Integracao com Outros Artefatos
- **ADRs**: toda decisao listada na secao 7 deve apontar para um ADR existente; atualizar reciprocamente o ADR com referencia ao KB.
- **Prompts**: mudancas em prompts devem ser refletidas tanto aqui (status e backlog) quanto em `prompts.canonical.md` e `docs/prompts.md`.
- **Roadmap**: horizonte de proximas etapas deve espelhar roadmap ativo; divergencias precisam ser justificadas e resolvidas no mesmo ciclo.

