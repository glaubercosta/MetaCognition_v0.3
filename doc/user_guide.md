# Guia do Usuário - MetaCognition v0.3

## Visão Geral
O MetaCognition é um orquestrador de agentes e fluxos. Esta versão (v0.3) introduz melhorias significativas na experiência de edição e segurança.

## Gerenciamento de Agentes

### Criando um Agente
1. Navegue até a página "Agents".
2. Clique em "Create Agent".
3. Preencha os campos:
    - **Name**: Nome do agente.
    - **Role**: Papel do agente (ex: "Engenheiro de Software").
    - **Goal**: Objetivo principal (suporta Markdown).
    - **Backstory**: História de fundo e personalidade (suporta Markdown).
    - **Tools**: Lista de ferramentas separadas por vírgula.
4. Use o editor Markdown para formatar o texto com negrito, listas, tabelas, etc.
5. Clique na aba "Preview" para visualizar como o texto será renderizado.
6. Clique em "Create Agent" para salvar.

### Editando um Agente
1. Na lista de agentes, clique no ícone de lápis (Edit) no cartão do agente desejado.
2. Modifique os campos conforme necessário.
3. Clique em "Update Agent".

## Segurança

### Rate Limiting
O sistema possui proteção contra excesso de requisições. Se você exceder o limite (100 requisições por minuto), receberá um erro `429 Too Many Requests`. Aguarde alguns instantes e tente novamente.

### Sanitização
Para sua segurança, tags HTML inseridas nos campos de texto serão removidas automaticamente. Use Markdown para formatação.
