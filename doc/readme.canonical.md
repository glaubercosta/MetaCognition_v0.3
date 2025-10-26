# README - Versao Canonica

## Proposito
Fornecer um guia oficial e conciso para novos colaboradores entenderem o objetivo do projeto, como instalar, operar e contribuir, alinhado aos demais artefatos canonicos.

## Estrutura Recomendada
1. **Visao Geral**: descricao curta do projeto, problema resolvido e principais capacidades.
2. **Funcionalidades Principais**: lista resumida com foco em valor entregue (extracao, analise, interface, exportacao, modos de execucao).
3. **Instalacao**: prerequisitos, passos para clonar, criar ambiente virtual, instalar dependencias e configurar variaveis de ambiente.
4. **Uso**: instrucoes para iniciar a aplicacao Streamlit e CLI (quando aplicavel), com fluxo basico de analise.
5. **Configuracoes Avancadas**: parametros chave, modelos utilizados e orientacoes de tuning.
6. **Estrutura de Saida**: formato dos arquivos gerados (CSV, logs) e campos relevantes.
7. **Arquitetura e Estrutura do Projeto**: diagrama ou arvore resumida dos arquivos principais com explicacao da camada.
8. **Solucoes de Problemas**: secao curta para erros comuns (API, rate limit, memoria).
9. **Contribuicao**: processo padrao de PR, testes e revisao.
10. **Licenca e Suporte**: referencia a licenca (ex. MIT) e canais de contato.

## Conteudos Obrigatorios
- Linkar para `docs/prompts.md`, `docs/PROJECT_KB.md` e `docs/adr/` para aprofundamento.
- Registrar versao do README e data da ultima revisao no cabecalho.
- Incluir tabela ou bullet com stack atual (Python 3.11+, Streamlit, OpenAI gpt-4o-mini, PyMuPDF, SQLite).
- Destacar requisitos de seguranca (armazenar chaves fora do repositorio).

## Processo de Atualizacao
1. Revisar o README ao final de cada release ou mudanca significativa de fluxo.
2. Garantir alinhamento com backlog e status descritos no KB.
3. Atualizar exemplos de comandos, caminhos de arquivos e instrucoes de setup conforme scripts evoluem.
4. Validar instrucoes em ambiente limpo antes de publicar alteracoes.

## Checklist Rapido
- [ ] Links e comandos verificados.
- [ ] Conteudo consistente com `docs/temp/project_kb.canonical.md`.
- [ ] Secao de funcionalidades alinhada com prompts ativos e ADRs vigentes.
- [ ] Estrutura de saida descreve campos e formatos atualizados.
- [ ] Referencias cruzadas para roadmap, prompts e ADRs presentes.

