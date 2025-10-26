# Catalogo de Prompts - Versao Canonica

## Objetivo
Garantir que o time tenha uma fonte unica e verificavel sobre prompts ativos, legados e regras de atualizacao, servindo como referencia oficial para alinhamento operacional.

## Estrutura do Documento
- **Header**: data da revisao, responsavel, link para PR ou issue que motivou a atualizacao.
- **Prompts Ativos**: tabela com nome, localizacao, versao/data, proposito, regras essenciais e observacoes criticas.
- **Prompts Legados**: lista controlada com justificativa para cada desuso.
- **Procedimentos e Boas Praticas**: instrucoes curtas para governanca dos prompts (registrar versoes, validar saidas, limites de historico).
- **Historico Enxuto**: log com no maximo N entradas recentes; entradas antigas devem ser movidas para `docs/history/prompts-log-YYYY.md`.

## Versao Atual (2025-02-19)

### Prompts Ativos
| Nome | Localizacao | Versao | Proposito | Regras Essenciais | Observacoes |
| ---- | ----------- | ------ | --------- | ----------------- | ----------- |
| Slim Extraction | `extraction_prompt_slim.py:1` | 2025-02-19 | Extrair requisitos de concorrentes ou TRT Base com alto foco em sinal | Apenas secoes elegiveis; um requisito por linha; preservar redacao original; usar sentinel quando nao houver dado | Ajustar `max_tokens` conforme volume; entrada reduzida por prefiltro de secoes |
| Analyst Slim (analise local) | `prompts.py:150` | 2025-02-19 | Fornecer contexto de analise local sem envio a LLM externa | Nao enviar como system prompt; exclusivo para pipelines internos | Validar consistencia ao ajustar variaveis de ambiente |
| KB Sync Agent | `docs/prompts.md#kb-sync-agent-versao-20250219` | 2025-02-19 | Coordenar sincronizacao manual entre KB, ADRs, roadmap e catalogo de prompts | Seguir fluxo definido; manter historico enxuto; checagem cruzada obrigatoria | Execucao manual; revisar saidas antes de aplicar mudancas |

### Prompts Legados / Fora do Fluxo Principal
- `EXTRACTION_PROMPT` (`prompts.py`) - substituido pela versao Slim por motivos de consistencia.
- `RAG_ANALYSIS_PROMPT` (`prompts.py`) - mantido apenas para referencia historica; ativacao sujeita a aprovacao previa.
- `get_extraction_query` (`prompts.py`) - helper descontinuado pelo novo pipeline de extracao.

## Procedimentos de Atualizacao
1. Identificar gatilho (PR, issue, release ou metrica) que demanda revisao de prompt.
2. Atualizar a tabela de prompts ativos com versao e link relevante.
3. Registrar mudancas no KB e no roadmap, quando aplicavel, garantindo referencias cruzadas.
4. Manter `docs/prompts.md` como copia operacional; esta versao canonica deve ser atualizada primeiro e depois consolidada nos demais artefatos.

## Boas Praticas
- Manter instrucoes objetivas e evitar frases ambiguas.
- Validar a saida dos prompts antes de disponibiliza-los para uso amplo.
- Registrar dependencias externas (datasets, pipelines) associadas ao prompt.
- Revisar e arquivar historicos conforme politica de retenção definida.
