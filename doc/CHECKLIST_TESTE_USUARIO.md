# Checklist de Teste de Usuário Final - MetaCognition v0.3

**Data da versão**: 2025-11-09  
**Objetivo**: Validar a experiência end-to-end do sistema antes de considerar o MVP pronto para release.

---

## Pré-requisitos

- [x] Sistema rodando via `docker compose up --build` OU backend local + frontend built
- [x] Frontend assets disponíveis em `public/` (rodar `.\scripts\frontend-build.ps1` no Windows ou `make frontend-all` no Unix/macOS)
- [x] Navegador com cache limpo ou DevTools → Network → "Disable cache" ativado
- [x] Acesso ao endpoint base: http://localhost:8000
- [x] Documentação da API disponível: http://localhost:8000/docs (Swagger/OpenAPI)

---

## 1. Health Check & Infraestrutura

### 1.1 Verificação Básica

- [x] **Health endpoint retorna OK**  

  ```powershell

  Invoke-RestMethod http://localhost:8000/health
  ```  Esperado: `{"status": "ok"}`

- [x] **Swagger UI carrega corretamente**
  
  Abrir <http://localhost:8000/docs>  
  Esperado: página interativa com todos os endpoints listados

- [x] **UI React carrega sem erros**  
  
  Abrir http://localhost:8000/  
  Esperado: interface gráfica visível, sem tela branca ou console errors (F12 → Console)

### 1.2 Performance Inicial

- [x] Tempo de carregamento da UI < 3 segundos (primeira carga)
- [x] Tempo de resposta do `/health` < 500ms
- [x] Assets estáticos (CSS/JS) servidos corretamente (verificar Network tab)

---

## 2. Gestão de Agentes (CRUD)

### 2.1 Criar Agente via UI

- [x] **Navegação**: clicar em "Agents" no menu lateral
- [x] **Criar novo agente**: botão "New Agent" ou similar visível e clicável
- [ ] **Formulário de criação**:
  - [-] Campos obrigatórios marcados claramente (nome, prompt, etc.)
  - [-] Validação inline para campos vazios ou inválidos
  - [ ] Limite de `PROMPT_MAX_BYTES` respeitado (mensagem de erro se excedido)
  - [x] Botão "Save" ou "Create" funcional
- [x] **Confirmação de criação**: agente aparece na lista após salvar
- [x] **ID gerado automaticamente** (UUID visível ou implícito)

### 2.2 Listar Agentes

- [x] **Lista carrega automaticamente** ao acessar a página de Agents
- [x] **Agentes de exemplo/seed** aparecem (se houver seed no banco)
- [x] **Dados exibidos**: nome, descrição resumida, ações (editar/excluir)
- [-] **Scroll funciona** se houver muitos agentes
- [ ] **Busca/filtro** (se implementado): testar com palavras-chave

### 2.3 Visualizar Detalhes de Agente

- [x] **Clicar em agente existente** abre view de detalhes ou modal
- [ ] **Todos os campos exibidos**: nome, prompt, role, tags, config JSON
- [-] **Formato legível** (JSON formatado, não raw string)
- [ ] **Botão "Edit"** disponível e funcional

### 2.4 Editar Agente

- [x] **Abrir editor**: clicar em "Edit" de um agente existente
- [-] **Editor Markdown**: verificar abas "Write" e "Preview"
- [-] **Preview em tempo real**: formatação (negrito, listas) aparece corretamente
- [x] **Formulário pré-preenchido** com dados atuais
- [x] **Modificar campo** (ex: alterar nome ou prompt)
- [x] **Salvar alteração**: botão "Save" funcional
- [x] **Verificar persistência**: recarregar página ou reabrir agente → mudança mantida
- [x] **Validação**: tentar salvar com campo obrigatório vazio → erro exibido

### 2.5 Excluir Agente

- [x] **Botão "Delete"** visível e clicável
- [x] **Confirmação antes de excluir** (modal "tem certeza?")
- [x] **Excluir confirmado**: agente removido da lista
- [x] **Verificar remoção do banco**: listar novamente ou via API → agente não aparece

### 2.6 Validação de Limites e Segurança

- [x] **Criar agente com prompt muito longo** (> `PROMPT_MAX_BYTES`) → erro de validação
- [x] **Criar agente com JSON de config inválido** → erro de validação
- [x] **Tentar acessar agente inexistente** via UI ou API → erro 404 tratado corretamente

---

## 3. Gestão de Fluxos (CRUD)

### 3.1 Criar Fluxo via UI

- [x] **Navegação**: clicar em "Flows" no menu
- [x] **Criar novo fluxo**: botão "New Flow" visível
- [ ] **Formulário de criação**:
  - [ ] Campos: nome, descrição, steps (JSON ou form)
  - [ ] Validação de estrutura de steps (array válido)
  - [ ] Referências a agentes válidos (se aplicável)
  - [x] Botão "Create" funcional
- [ ] **Fluxo criado** aparece na lista

### 3.2 Listar Fluxos

- [x] **Lista carrega automaticamente**
- [-] **Fluxos de exemplo/seed** visíveis (se houver)
- [-] **Dados exibidos**: nome, descrição, quantidade de steps, ações

### 3.3 Visualizar Detalhes de Fluxo

- [x] **Clicar em fluxo** abre detalhes
- [-] **Steps exibidos de forma estruturada** (não raw JSON, se possível)
- [x] **Referências a agentes** mostradas corretamente
- [x] **Botão "Edit"** disponível

### 3.4 Editar Fluxo

- [x] **Abrir editor de fluxo**
- [-] **Modificar steps** (adicionar/remover/reordenar)
- [x] **Salvar mudanças** → persistência confirmada
- [-] **Validação**: tentar salvar fluxo com steps inválidos → erro

### 3.5 Excluir Fluxo

- [x] **Botão "Delete"** funcional com confirmação
- [x] **Fluxo removido** da lista após confirmação

### 3.6 Orquestração de Fluxo

- [-] **Botão "Run" ou "Execute"** visível na página de detalhes do fluxo
- [-] **Executar fluxo**: clicar em "Run"
- [-] **Feedback de execução**: loading spinner ou status "running"
- [-] **Resultado exibido**: artifacts, logs, runId gerado
- [-] **Verificar engine usado**: logs mostram qual adapter foi acionado (fake, langchain, etc.)

---

## 4. Import/Export de Artefatos

### 4.1 Export de Agentes

- [ ] **Navegação**: menu "Import/Export" ou similar
- [ ] **Botão "Export Agents"** visível
- [ ] **Selecionar formato**: JSON ou YAML
- [ ] **Download iniciado**: arquivo `.json` ou `.yaml` baixado
- [ ] **Abrir arquivo exportado**: estrutura válida, contém agentes esperados
- [ ] **Validar schema**: arquivo segue `ProjectArtifacts/schemas/agent-schema.json`

### 4.2 Export de Fluxos

- [ ] **Botão "Export Flows"** visível
- [ ] **Selecionar formato**: JSON ou YAML
- [ ] **Download iniciado**
- [ ] **Abrir arquivo exportado**: estrutura válida, contém fluxos esperados
- [ ] **Validar schema**: arquivo segue `ProjectArtifacts/schemas/flow-schema.json`

### 4.3 Import de Agentes (JSON)

- [ ] **Botão "Import Agents"** visível
- [ ] **Upload de arquivo JSON**: selecionar arquivo válido
- [ ] **Validação inline**: se arquivo inválido, erro exibido antes de submit
- [ ] **Import confirmado**: mensagem de sucesso + quantidade de agentes importados
- [ ] **Verificar persistência**: agentes importados aparecem na lista de Agents

### 4.4 Import de Agentes (YAML)

- [ ] **Upload de arquivo YAML**
- [ ] **Import bem-sucedido**: parsing YAML → JSON → persistência
- [ ] **Agentes importados** visíveis na lista

### 4.5 Import de Fluxos (JSON/YAML)

- [ ] **Upload de arquivo de fluxos (JSON ou YAML)**
- [ ] **Import confirmado**
- [ ] **Fluxos importados** aparecem na lista de Flows

### 4.6 Validação e Limites de Import

- [ ] **Arquivo muito grande** (> `IMPORT_MAX_FILE_MB`) → erro de validação antes de processar
- [ ] **Muitos itens** (> `IMPORT_MAX_ITEMS`) → erro de validação
- [ ] **JSON malformado** → erro claro exibido ao usuário
- [ ] **YAML malformado** → erro claro exibido
- [ ] **Schema inválido** (falta campos obrigatórios) → erro de validação com detalhes

### 4.7 Endpoint de Validação Prévia

- [ ] **Testar via Swagger**: `POST /agents/validate` com payload JSON
- [ ] **Payload válido** → resposta 200 com confirmação
- [ ] **Payload inválido** → resposta 422 com erros detalhados
- [ ] **Mesmo teste para** `POST /flows/validate`

---

## 5. Conversão Markdown → JSON

### 5.1 Converter Agente de Markdown via UI

- [ ] **Navegação**: página "Import/Export" ou "Convert"
- [ ] **Campo de texto ou upload** para Markdown
- [ ] **Inserir exemplo de Markdown** (usar template de `ProjectArtifacts/examples/` se disponível)
- [ ] **Botão "Convert to JSON"** visível
- [ ] **Conversão bem-sucedida**: JSON exibido na tela
- [ ] **JSON gerado válido**: copiar e validar contra schema
- [ ] **Opção "Save as Agent"**: salvar diretamente no banco após conversão

### 5.2 Converter via API (Swagger)

- [ ] **Abrir Swagger**: http://localhost:8000/docs
- [ ] **Endpoint**: `POST /convert/agent-md`
- [ ] **Body**: colar Markdown de exemplo
- [ ] **Executar**: resposta 200 com JSON
- [ ] **JSON retornado** válido e completo

---

## 6. Orquestração e Execução

### 6.1 Executar Fluxo Simples (Stub/Fake)

- [ ] **Garantir engine configurado**: `DEFAULT_ENGINE=fake` em `.env` (ou stub)
- [ ] **Criar fluxo de teste** (ou usar fluxo existente)
- [ ] **Executar via UI**: botão "Run" na página de Flow
- [ ] **Resultado retornado**: `runId`, `status`, `artifacts`
- [ ] **Tempo de resposta** < 5 segundos (para fake engine)
- [ ] **Logs/trace** visíveis (se UI mostra)

### 6.2 Executar com Engine LangChain (se configurado)

- [ ] **Configurar `.env`**: `DEFAULT_ENGINE=langchain`, `LANGCHAIN_PROVIDER=stub` (ou OpenAI se tiver key)
- [ ] **Reiniciar serviço** para aplicar config
- [ ] **Executar fluxo**
- [ ] **Resultado retornado**: estrutura `OrchestrationResult` válida
- [ ] **Logs mostram** provider usado (stub, openai, etc.)
- [ ] **Se OpenAI real**: verificar chamada externa e resposta coerente

### 6.3 Validação de Erros de Orquestração

- [ ] **Executar fluxo com agente inexistente** → erro 404 ou mensagem clara
- [ ] **Executar fluxo com steps mal-formados** → erro de validação
- [ ] **Executar com engine desconhecido** (forçar via API) → erro 400 ou 500 tratado

---

## 7. Avaliações (Stub)

### 7.1 Listar Avaliações

- [ ] **Navegação**: menu "Evaluations" ou similar
- [ ] **Lista de avaliações** visível (pode estar vazia ou com seed)
- [ ] **Se houver avaliações**, exibir: ID, status, data, score

### 7.2 Criar Avaliação (se endpoint disponível)

- [ ] **Botão "New Evaluation"** ou similar
- [ ] **Formulário**: referenciar agente/flow, critérios
- [ ] **Criar**: avaliação persistida
- [ ] **Verificar**: avaliação aparece na lista

### 7.3 Validação de Stub

- [ ] **Verificar que avaliações não fazem chamadas externas** (modo stub)
- [ ] **Resultados determinísticos** (se stub, sempre mesmo output)

---

## 8. Configurações e Variáveis de Ambiente

### 8.1 Verificar Aplicação de Limites

- [ ] **`IMPORT_MAX_FILE_MB`**: testar upload > limite → erro antes de processar
- [ ] **`IMPORT_MAX_ITEMS`**: importar arquivo com muitos itens → erro de validação
- [ ] **`PROMPT_MAX_BYTES`**: criar agente com prompt > limite → erro de validação

### 8.2 Trocar Engine em Runtime (requer restart)

- [ ] **Editar `.env`**: `DEFAULT_ENGINE=fake`
- [ ] **Reiniciar**: `docker compose restart` ou restart manual
- [ ] **Executar fluxo**: verificar que engine `fake` é usado
- [ ] **Trocar para `langchain`** (com provider stub)
- [ ] **Reiniciar e executar**: verificar que engine mudou

### 8.3 Configuração de Logs

- [ ] **`LOG_LEVEL=DEBUG`**: reiniciar e verificar logs detalhados no stdout
- [ ] **`LOG_LEVEL=INFO`**: logs mais enxutos
- [ ] **Logs estruturados**: JSON ou formato legível

---

## 9. Navegação e UX

### 9.1 Menu Lateral / Navegação

- [ ] **Menu visível e responsivo**
- [ ] **Links funcionais**: Agents, Flows, Orchestration, Evaluations, Import/Export, Settings
- [ ] **Highlight de página ativa** (item de menu marcado quando na página)
- [ ] **Mobile/responsivo** (se aplicável): menu colapsa em telas pequenas

### 9.2 Feedback Visual

- [ ] **Loading spinners** durante operações assíncronas (criar, executar, importar)
- [ ] **Mensagens de sucesso** após operações bem-sucedidas (toasts, alerts)
- [ ] **Mensagens de erro** claras e acionáveis quando algo falha
- [ ] **Validação inline** em formulários (campo fica vermelho, mensagem abaixo)

### 9.3 Consistência de Design

- [ ] **Tema visual aplicado** (dark/light mode se disponível)
- [ ] **Tipografia legível** (tamanhos, contraste)
- [ ] **Espaçamento consistente** entre componentes
- [ ] **Botões com estados visuais** (hover, active, disabled)

---

## 10. Segurança e Robustez

### 10.1 Injeção e Sanitização

- [x] **Criar agente com script malicioso no prompt** (ex: `<script>alert('xss')</script>`)  
  → Verificar que UI não executa script (HTML escapado/removido pelo backend)
- [x] **Criar agente com JSON de config malformado** → erro de validação tratado
- [ ] **Importar arquivo com payload malicioso** (se possível testar) → validação/sanitização aplicada

### 10.2 Rate Limiting e DoS (básico)

- [x] **Enviar múltiplas requisições rápidas** (ex: criar 100 agentes em loop)  
  → Sistema responde sem crashar (retorna 429 Too Many Requests após 100 req/min)

### 10.3 Recuperação de Erros

- [ ] **Matar container durante execução de fluxo** → ao reiniciar, sistema volta ao estado consistente
- [ ] **Corromper `.db` (backup primeiro!)** → sistema detecta erro e retorna mensagem, não crasha silenciosamente

---

## 11. Documentação e Onboarding

### 11.1 README e Guias

- [ ] **README.md** atualizado com instruções claras de setup
- [ ] **Comandos copyable** funcionam (PowerShell e Unix)
- [ ] **Pré-requisitos listados** (Docker, Node.js, etc.)
- [ ] **Troubleshooting básico** documentado (ex: UI em branco → cache)

### 11.2 Swagger/OpenAPI

- [ ] **Swagger UI** acessível e completo
- [ ] **Todos os endpoints documentados** com descrições
- [ ] **Exemplos de request/response** visíveis
- [ ] **Esquemas de dados** (schemas) disponíveis

### 11.3 Exemplos e Templates

- [ ] **`ProjectArtifacts/examples/`**: verificar se há exemplos de agentes/fluxos
- [ ] **Importar exemplo oficial** via UI → import bem-sucedido
- [ ] **Executar exemplo oficial** → resultado esperado

---

## 12. Testes de Integração (Manual via Cenário Completo)

### Cenário End-to-End: "Criar, Importar, Executar e Avaliar"

1. **Setup Inicial**
   - [ ] Limpar banco de dados (deletar `data/app.db` e reiniciar)
   - [ ] Serviço rodando limpo (sem dados prévios)

2. **Criar Agente via UI**
   - [ ] Criar agente "Analista de Dados" com prompt específico
   - [ ] Confirmar criação na lista

3. **Criar Fluxo Referenciando Agente**
   - [ ] Criar fluxo "Pipeline de Análise" com 2 steps
   - [ ] Step 1: usar agente "Analista de Dados"
   - [ ] Step 2: usar agente stub (ou criar segundo agente)
   - [ ] Salvar fluxo

4. **Exportar Artefatos**
   - [ ] Exportar agentes para JSON
   - [ ] Exportar fluxos para YAML
   - [ ] Baixar e verificar conteúdo dos arquivos

5. **Limpar e Reimportar**
   - [ ] Deletar agente e fluxo via UI
   - [ ] Confirmar que lista está vazia
   - [ ] Importar arquivos salvos anteriormente
   - [ ] Confirmar que agente e fluxo voltaram

6. **Executar Fluxo Importado**
   - [ ] Abrir fluxo reimportado
   - [ ] Clicar "Run"
   - [ ] Verificar resultado: runId, artifacts, status "completed"
   - [ ] Logs/trace visíveis (se disponível)

7. **Converter Markdown → JSON → Criar Agente**
   - [ ] Ir para tela de conversão
   - [ ] Colar Markdown de exemplo
   - [ ] Converter para JSON
   - [ ] Salvar como novo agente
   - [ ] Confirmar que agente aparece na lista

8. **Validar Avaliação (Stub)**
   - [ ] Criar avaliação para o fluxo executado (se endpoint disponível)
   - [ ] Verificar que avaliação foi persistida
   - [ ] Listar avaliações → nova avaliação visível

9. **Testar Limites**
   - [ ] Tentar importar arquivo > `IMPORT_MAX_FILE_MB` → erro
   - [ ] Tentar criar agente com prompt > `PROMPT_MAX_BYTES` → erro

10. **Finalizar**
    - [ ] Todas as operações funcionaram sem crashes
    - [ ] UI permaneceu responsiva
    - [ ] Mensagens de erro/sucesso foram claras

---

## 13. Performance e Escalabilidade (Básico)

### 13.1 Volume de Dados

- [ ] **Criar 50 agentes** via API ou script → listar todos sem travar UI
- [ ] **Criar 20 fluxos** → navegação permanece fluida
- [ ] **Executar 10 fluxos em sequência** → sistema responde sem degradação significativa

### 13.2 Tempo de Resposta

- [ ] **GET /agents**: < 1 segundo para lista de ~50 agentes
- [ ] **POST /agents**: < 500ms para criar agente
- [ ] **POST /orchestrate/run** (fake engine): < 3 segundos

---

## 14. Compatibilidade de Navegador

- [ ] **Chrome/Edge**: todas as funcionalidades OK
- [ ] **Firefox**: UI carrega e funciona
- [ ] **Safari** (se disponível): testar carregamento e CRUD básico

---

## 15. Observabilidade e Debugging

### 15.1 Logs do Sistema

- [x] **Logs estruturados** visíveis no stdout do container (JSON format)
- [x] **Request ID** presente em cada log (`request_id`)
- [x] **Erros logados** com stack trace quando falhas ocorrem
- [x] **Logs de orquestração** mostram engine usado, duration_ms, status

### 15.2 DevTools (Browser)

- [ ] **Console sem erros** (F12 → Console) na carga inicial da UI
- [ ] **Network tab**: requisições retornam 200/201 para operações bem-sucedidas
- [ ] **Network tab**: erros (4xx/5xx) têm response body com detalhes do erro

---

## 16. Rollback e Recuperação

- [ ] **Backup de `.db`**: fazer backup de `data/app.db` antes de testes destrutivos
- [ ] **Restaurar backup**: copiar backup de volta → sistema volta ao estado anterior
- [ ] **Teste de crash**: matar container (`docker kill orchestrator`) e reiniciar → sistema volta funcional

---

## 17. Verificação de Staging (Sprint 4)

- [x] **Ambiente Staging Rodando**: `docker compose -f docker-compose.yml -f docker-compose.staging.yml up`
- [x] **Variáveis de Ambiente**: `APP_ENV=staging` confirmado nos logs
- [x] **CORS Restrito**: Acesso bloqueado de origens não permitidas (testar via curl com Origin diferente)
- [x] **Frontend Build**: Assets servidos corretamente em `/`
- [x] **Health Check**: `curl http://localhost:8000/health` retorna 200 OK

---

## Critérios de Aceite Global

Para considerar o MVP pronto para release, **TODOS** os itens críticos abaixo devem estar ✅:

- [ ] **Health endpoint** retorna OK consistentemente
- [ ] **UI carrega** sem erros de console
- [ ] **CRUD de agentes** funciona completamente (criar, listar, editar, excluir)
- [ ] **CRUD de fluxos** funciona completamente
- [ ] **Import/Export** (JSON e YAML) funciona para agentes e fluxos
- [ ] **Validação de limites** aplicada corretamente (tamanho, quantidade, bytes)
- [ ] **Orquestração** executa fluxos e retorna resultados válidos (pelo menos com engine fake)
- [ ] **Conversão Markdown → JSON** funciona e persiste agentes
- [ ] **Swagger/docs** acessível e completo
- [ ] **Mensagens de erro** claras e acionáveis (não crashes silenciosos)
- [ ] **Performance aceitável** (< 3s para operações típicas)
- [ ] **README atualizado** com instruções funcionais

---

## Notas Finais

- **Reporte de bugs**: anotar comportamento inesperado, erros de console, screenshots
- **Sugestões de UX**: listar melhorias identificadas durante teste (ex: falta de confirmação, labels confusas)
- **Priorização**: focar primeiro em fluxos críticos (criar, importar, executar) antes de edge cases
- **Ambiente de teste**: garantir que `.env` está configurado corretamente e frontend foi built (`make frontend-all` ou `.\scripts\frontend-build.ps1`)

**Boa sorte com os testes! 🚀**

---

## Relatório de desconformidade

- **Report de Bugs**

- É possível fazer a exclusão de um Agente que já esteja atrelado a um fluxo. Isso não pode acontecer: o correto é indicar que o agente já está sendo utilizado em um fluxo e orientar que, para excluir o agente em definitivo deve-se retirar o agente de todos os fluxos aos quais ele esteja associado.
- O número de agentes de um fluxo não está sendo atualizado quando um determinado agente é excluído.

- **Sugestoes de UX**

- ### 2.1

- Os campos obrigatórios não estão identificados.
  
- ### 2.2
  
- Filtro/Busca nao implementado

- ### 2.3

- O formulario de criacao/edicao de agentes nao está responsivo. Para visualiza-lo completamente é necessário reduzir o zoom do navegador.

- ### 3.1

- Nao foi implementado a possibilidade de gerenciar os passos do fluxo (qual agente sucede outro) e nem o que deve acontecer em caso de erros entre os agentes.
