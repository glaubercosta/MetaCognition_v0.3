# Guia de Integração do Design - MetaCognition v0.3

## 📋 Visão Geral

Este guia detalha o processo completo para integrar o design moderno criado no Lovable ao seu projeto MetaCognition_v0.3 no GitHub, mantendo toda a funcionalidade do backend FastAPI.

---

## 🎯 Estrutura de Arquivos a Copiar

### 1. Componentes Reutilizáveis

Copie os seguintes arquivos de `src/components/` do Lovable para seu projeto GitHub:

```
src/components/
├── StatCard.tsx          # Cards de estatísticas do dashboard
├── AgentCard.tsx         # Cards para exibir agentes
├── FlowCard.tsx          # Cards para exibir fluxos
├── EmptyState.tsx        # Estado vazio com ícone e mensagem
├── PageHeader.tsx        # Header de páginas com título e ações
└── AppSidebar.tsx        # Sidebar de navegação
```

### 2. Componentes UI (shadcn/ui)

Copie toda a pasta `src/components/ui/` que contém os componentes base:

```
src/components/ui/
├── button.tsx
├── card.tsx
├── badge.tsx
├── dialog.tsx
├── input.tsx
├── label.tsx
├── select.tsx
├── textarea.tsx
├── toast.tsx
├── toaster.tsx
├── sidebar.tsx
└── ... (todos os outros componentes)
```

### 3. Páginas Refatoradas

Copie todos os arquivos de `src/pages/`:

```
src/pages/
├── Dashboard.tsx         # Dashboard com cards de estatísticas
├── Agents.tsx           # Listagem e gerenciamento de agentes
├── Flows.tsx            # Listagem e gerenciamento de fluxos
├── Orchestration.tsx    # Execução de orquestrações
├── Evaluations.tsx      # Visualização de avaliações
├── ImportExport.tsx     # Import/Export de dados
├── Settings.tsx         # Configurações do sistema
├── Index.tsx            # Página inicial
└── NotFound.tsx         # Página 404
```

### 4. Utilitários e Configurações

```
src/lib/
├── utils.ts             # Helper function cn() para classes
└── api.ts               # Cliente API (adapte as URLs para seu backend)

src/hooks/
├── use-mobile.tsx       # Hook para detectar mobile
└── use-toast.ts         # Hook para notificações toast
```

### 5. Estilos e Configuração

```
src/index.css            # Design tokens HSL e estilos globais
src/App.tsx              # Componente principal com roteamento
src/App.css              # Estilos do App
src/main.tsx             # Entry point do React
tailwind.config.ts       # Configuração do Tailwind com tema
vite.config.ts           # Configuração do Vite
```

---

## 📦 Instalação de Dependências

### 1. Instalar Dependências do React e UI

```bash
npm install react react-dom react-router-dom
npm install @tanstack/react-query
npm install lucide-react
npm install sonner
npm install date-fns
```

### 2. Instalar Componentes Radix UI (shadcn)

```bash
npm install @radix-ui/react-slot
npm install @radix-ui/react-dialog
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-select
npm install @radix-ui/react-toast
npm install @radix-ui/react-label
npm install @radix-ui/react-separator
npm install @radix-ui/react-accordion
npm install @radix-ui/react-alert-dialog
npm install @radix-ui/react-avatar
npm install @radix-ui/react-checkbox
npm install @radix-ui/react-tabs
npm install @radix-ui/react-switch
npm install @radix-ui/react-popover
npm install @radix-ui/react-scroll-area
```

### 3. Instalar Tailwind CSS e Utilitários

```bash
npm install -D tailwindcss postcss autoprefixer
npm install tailwindcss-animate
npm install class-variance-authority
npm install clsx tailwind-merge
```

### 4. Instalar Vite e TypeScript

```bash
npm install -D vite @vitejs/plugin-react-swc
npm install -D typescript @types/react @types/react-dom
```

---

## ⚙️ Configuração do Projeto

### 1. Inicializar Tailwind CSS

```bash
npx tailwindcss init -p
```

### 2. Configurar tsconfig.json

Crie ou atualize o `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 3. Configurar package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  }
}
```

### 4. Criar postcss.config.js

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

---

## 🔗 Integração com FastAPI

### 1. Estrutura de Diretórios

```
seu-projeto/
├── backend/
│   ├── main.py
│   ├── api/
│   └── ...
├── frontend/              # Novo: projeto React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
└── public/               # Arquivos estáticos servidos pelo FastAPI
```

### 2. Build do Frontend

Execute no diretório `frontend/`:

```bash
npm run build
```

Isso gera os arquivos otimizados em `frontend/dist/`.

### 3. Copiar Arquivos para o Backend

```bash
# Linux/Mac
cp -r frontend/dist/* public/

# Windows (PowerShell)
Copy-Item -Path "frontend\dist\*" -Destination "public\" -Recurse -Force
```

### 4. Configurar FastAPI para Servir o React

Atualize seu `main.py`:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="MetaCognition API", version="0.3")

# Suas rotas de API existentes
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# ... outras rotas da API ...

# Servir arquivos estáticos do React
app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")

# Rota catch-all para o React Router
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """
    Serve o React app para todas as rotas não-API.
    Permite que o React Router funcione corretamente.
    """
    # Se for uma rota de API, não interceptar
    if full_path.startswith("api/"):
        return {"error": "Not found"}, 404
    
    # Verificar se é um arquivo estático
    file_path = os.path.join("public", full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Caso contrário, servir o index.html (React Router)
    return FileResponse("public/index.html")
```

### 5. Atualizar URLs da API no Frontend

No arquivo `src/lib/api.ts`, atualize a `API_BASE_URL`:

```typescript
// Desenvolvimento
const API_BASE_URL = 'http://localhost:8000/api';

// Produção (ajuste conforme necessário)
// const API_BASE_URL = '/api';
```

---

## 🚀 Executando o Projeto

### Modo Desenvolvimento

#### Terminal 1 - Backend FastAPI
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### Terminal 2 - Frontend React (opcional durante dev)
```bash
cd frontend
npm run dev
```

**Nota:** Durante o desenvolvimento, você pode usar o Vite dev server na porta 5173 e fazer proxy das chamadas de API para o backend na porta 8000.

### Modo Produção

1. **Build do Frontend:**
```bash
cd frontend
npm run build
cp -r dist/* ../public/
```

2. **Executar Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

3. **Acessar:** `http://localhost:8000`

---

## 🎨 Design System - Tokens CSS

O design usa tokens HSL definidos em `src/index.css`. **IMPORTANTE:** Sempre use tokens semânticos, nunca cores diretas:

### ✅ Correto:
```tsx
<div className="bg-primary text-primary-foreground">
<div className="text-muted-foreground">
<div className="border-border">
```

### ❌ Errado:
```tsx
<div className="bg-blue-500 text-white">
<div className="text-gray-600">
<div className="border-gray-300">
```

### Tokens Principais:

```css
--background: 0 0% 100%;           /* Fundo principal */
--foreground: 240 10% 3.9%;        /* Texto principal */
--primary: 240 5.9% 10%;           /* Cor primária */
--secondary: 240 4.8% 95.9%;       /* Cor secundária */
--muted: 240 4.8% 95.9%;           /* Cor muted */
--accent: 240 4.8% 95.9%;          /* Cor de destaque */
--destructive: 0 84.2% 60.2%;      /* Cor de erro/deletar */
--border: 240 5.9% 90%;            /* Bordas */
```

---

## 📱 Responsividade

Todos os componentes são responsivos usando breakpoints do Tailwind:

```tsx
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
```

Breakpoints:
- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px
- `2xl:` 1536px

---

## ♿ Acessibilidade

O design segue boas práticas de acessibilidade (WCAG):

- ✅ Tags semânticas HTML5
- ✅ ARIA labels e roles
- ✅ Contraste adequado de cores
- ✅ Navegação por teclado
- ✅ Suporte a screen readers

Exemplo:
```tsx
<button aria-label="Edit agent" onClick={handleEdit}>
  <Pencil className="h-4 w-4" aria-hidden="true" />
</button>
```

---

## 🔧 Adaptações Necessárias

### 1. Ajustar Endpoints da API

Verifique se os endpoints em `src/lib/api.ts` correspondem aos do seu backend:

```typescript
// Exemplo atual
export const getAgents = async (): Promise<Agent[]> => {
  const response = await fetch(`${API_BASE_URL}/agents`);
  // ...
};

// Ajuste para seu backend se necessário
```

### 2. Adaptar Modelos de Dados

Se seus modelos de dados forem diferentes, ajuste as interfaces em `src/lib/api.ts`:

```typescript
export interface Agent {
  id?: string;
  name: string;
  role: string;
  goal: string;
  backstory?: string;
  tools?: string[];
}
```

### 3. Configurar CORS no Backend

Certifique-se de que o FastAPI aceita requisições do frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Componentes Principais

### StatCard
Exibe estatísticas com ícone e valor:
```tsx
<StatCard
  title="Total Agents"
  value={agents.length}
  icon={Bot}
  trend={{ value: "+12%", positive: true }}
/>
```

### AgentCard
Card para exibir um agente:
```tsx
<AgentCard
  agent={agent}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### FlowCard
Card para exibir um fluxo:
```tsx
<FlowCard
  flow={flow}
  agentNames="Agent 1, Agent 2"
/>
```

### EmptyState
Estado vazio com call-to-action:
```tsx
<EmptyState
  icon={Bot}
  title="No agents yet"
  description="Create your first agent to get started"
  actionLabel="Create Agent"
  onAction={openDialog}
/>
```

### PageHeader
Header de página com título e ação:
```tsx
<PageHeader
  title="Agents"
  description="Manage your AI agents"
  action={<Button onClick={openDialog}>Create Agent</Button>}
/>
```

---

## 🐛 Troubleshooting

### Erro: "Cannot find module '@/...'"

**Solução:** Certifique-se de que o alias `@` está configurado no `vite.config.ts`:

```typescript
import path from "path";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Erro: Estilos do Tailwind não aplicados

**Solução:** Verifique o `tailwind.config.ts`:

```typescript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  // ...
}
```

### Erro 404 nas rotas do React

**Solução:** Configure a rota catch-all no FastAPI (veja seção "Integração com FastAPI").

### API CORS Error

**Solução:** Configure o middleware CORS no FastAPI (veja seção "Adaptações Necessárias").

---

## 📝 Checklist de Integração

- [ ] Copiar todos os arquivos de `src/components/`
- [ ] Copiar todos os arquivos de `src/pages/`
- [ ] Copiar `src/lib/utils.ts` e `src/lib/api.ts`
- [ ] Copiar `src/index.css` e `tailwind.config.ts`
- [ ] Instalar todas as dependências
- [ ] Configurar `tsconfig.json` e `vite.config.ts`
- [ ] Ajustar URLs da API em `src/lib/api.ts`
- [ ] Configurar CORS no FastAPI
- [ ] Fazer build do frontend (`npm run build`)
- [ ] Copiar `dist/` para `public/`
- [ ] Configurar rota catch-all no FastAPI
- [ ] Testar todas as funcionalidades

---

## 🎉 Pronto!

Após seguir todos os passos, seu projeto MetaCognition_v0.3 terá:

✅ Design moderno e responsivo  
✅ Componentes reutilizáveis e modulares  
✅ Acessibilidade (WCAG)  
✅ Design system consistente  
✅ Integração completa com FastAPI  
✅ Funcionalidade preservada  

---

## 📞 Suporte

Se encontrar problemas durante a integração, revise:

1. Console do navegador (F12) para erros JavaScript
2. Logs do FastAPI para erros de backend
3. Network tab para verificar chamadas de API
4. Configuração do CORS

**Dica:** Durante o desenvolvimento, use o React DevTools e o React Query DevTools para debugging.

---

*Documentação gerada para MetaCognition v0.3 - Design System Lovable*
