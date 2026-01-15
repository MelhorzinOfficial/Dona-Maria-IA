# Story 1.1: Setup Inicial do Projeto

Status: review

## Story

As a **desenvolvedor**,
I want **ter o projeto configurado com a stack definida na arquitetura**,
So that **possa começar a implementar features com a estrutura correta**.

## Acceptance Criteria

1. **Given** um novo repositório vazio
   **When** o setup inicial é executado
   **Then** o projeto contém:

   - Frontend Next.js 15 com App Router configurado
   - Backend FastAPI com estrutura de pastas conforme arquitetura
   - Docker Compose funcional com PostgreSQL e Redis
   - Variáveis de ambiente de exemplo (.env.example)
   - ESLint, Prettier e TypeScript configurados no frontend
   - Ruff e MyPy configurados no backend

2. **Given** projeto com Docker Compose configurado
   **When** `docker-compose up` é executado
   **Then** todos os serviços iniciam sem erros
   **And** frontend acessível em localhost:3000
   **And** backend acessível em localhost:8000/docs (Swagger)

## Tasks / Subtasks

- [x] **Task 1: Estrutura Base do Repositório** (AC: #1)

  - [x] 1.1 Criar estrutura de pastas raiz (`frontend/`, `backend/`, `docker/`)
  - [x] 1.2 Criar README.md principal com instruções de setup
  - [x] 1.3 Criar `.gitignore` apropriado para monorepo Python + Node

- [x] **Task 2: Setup Frontend Next.js 15** (AC: #1)

  - [x] 2.1 Inicializar projeto Next.js 15 com App Router (`npx create-next-app@latest`)
  - [x] 2.2 Configurar TypeScript 5.x com strict mode
  - [x] 2.3 Instalar e configurar Tailwind CSS 4.x com tema customizado
  - [x] 2.4 Configurar ESLint com regras recomendadas Next.js + TypeScript
  - [x] 2.5 Configurar Prettier com integração ESLint
  - [x] 2.6 Criar estrutura de pastas conforme arquitetura (`app/`, `components/`, `lib/`, `hooks/`)
  - [x] 2.7 Configurar path aliases no tsconfig (`@/components`, `@/lib`, etc.)
  - [x] 2.8 Criar `.env.local.example` com variáveis necessárias

- [x] **Task 3: Setup Backend FastAPI** (AC: #1)

  - [x] 3.1 Inicializar projeto Python com `pyproject.toml` (Poetry ou uv)
  - [x] 3.2 Instalar dependências core: FastAPI 0.115+, Uvicorn, Pydantic 2.x
  - [x] 3.3 Instalar dependências de qualidade: Ruff, MyPy, pytest
  - [x] 3.4 Criar estrutura de pastas conforme arquitetura:
    ```
    backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config/
    │   │   ├── __init__.py
    │   │   └── settings.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── v1/
    │   │       ├── __init__.py
    │   │       └── router.py
    │   ├── models/
    │   │   └── __init__.py
    │   ├── services/
    │   │   └── __init__.py
    │   └── schemas/
    │       └── __init__.py
    ├── tests/
    │   └── __init__.py
    ├── pyproject.toml
    └── .env.example
    ```
  - [x] 3.5 Configurar Ruff com regras recomendadas (ruff.toml)
  - [x] 3.6 Configurar MyPy com strict mode (mypy.ini ou pyproject.toml)
  - [x] 3.7 Criar `main.py` com app FastAPI básico e health check endpoint
  - [x] 3.8 Criar `settings.py` com Pydantic Settings para carregar envvars

- [x] **Task 4: Docker Compose Development** (AC: #1, #2)

  - [x] 4.1 Criar `docker-compose.yml` com serviços: frontend, backend, postgres, redis
  - [x] 4.2 Criar `Dockerfile.dev` para frontend com hot reload
  - [x] 4.3 Criar `Dockerfile.dev` para backend com hot reload (Uvicorn --reload)
  - [x] 4.4 Configurar volumes para code syncing em dev
  - [x] 4.5 Configurar PostgreSQL 16-alpine com credenciais padrão
  - [x] 4.6 Configurar Redis 7-alpine
  - [x] 4.7 Criar `.env.example` na raiz com todas as variáveis necessárias

- [x] **Task 5: Validação e Documentação** (AC: #2)
  - [x] 5.1 Testar `docker-compose up` e validar todos os serviços
  - [x] 5.2 Validar frontend em http://localhost:3000
  - [x] 5.3 Validar backend Swagger em http://localhost:8000/docs
  - [x] 5.4 Validar conexão PostgreSQL e Redis
  - [x] 5.5 Atualizar README com instruções de desenvolvimento

## Dev Notes

### Stack Técnica Obrigatória

| Componente         | Tecnologia   | Versão | Notas                      |
| ------------------ | ------------ | ------ | -------------------------- |
| Frontend Framework | Next.js      | 15.x   | App Router obrigatório     |
| React              | React        | 19.x   | Concurrent features        |
| TypeScript         | TypeScript   | 5.x    | Strict mode                |
| CSS                | Tailwind CSS | 4.x    | Design system customizável |
| Backend Framework  | FastAPI      | 0.115+ | Async nativo               |
| Python             | Python       | 3.12+  | Ecossistema ML/AI          |
| Validação          | Pydantic     | 2.x    | Models e Settings          |
| Database           | PostgreSQL   | 16     | Alpine image               |
| Cache              | Redis        | 7      | Alpine image               |

### Estrutura de Pastas Final Esperada

```
dona-maria-ia/
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   ├── public/
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── .eslintrc.json
│   ├── .prettierrc
│   ├── Dockerfile.dev
│   └── .env.local.example
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── schemas/
│   ├── tests/
│   ├── pyproject.toml
│   ├── ruff.toml
│   ├── Dockerfile.dev
│   └── .env.example
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

### Configuração Docker Compose

Conforme arquitetura, usar a seguinte configuração base:

```yaml
version: '3.8'

services:
 frontend:
  build:
   context: ./frontend
   dockerfile: Dockerfile.dev
  ports:
   - '3000:3000'
  volumes:
   - ./frontend:/app
   - /app/node_modules
  environment:
   - NEXT_PUBLIC_API_URL=http://localhost:8000
   - NEXT_PUBLIC_WS_URL=ws://localhost:8000
  depends_on:
   - backend

 backend:
  build:
   context: ./backend
   dockerfile: Dockerfile.dev
  ports:
   - '8000:8000'
  volumes:
   - ./backend:/app
  environment:
   - DATABASE_URL=postgresql://dona:maria@postgres:5432/donamaria
   - REDIS_URL=redis://redis:6379
  depends_on:
   - postgres
   - redis

 postgres:
  image: postgres:16-alpine
  ports:
   - '5432:5432'
  environment:
   - POSTGRES_USER=dona
   - POSTGRES_PASSWORD=maria
   - POSTGRES_DB=donamaria
  volumes:
   - postgres_data:/var/lib/postgresql/data

 redis:
  image: redis:7-alpine
  ports:
   - '6379:6379'

volumes:
 postgres_data:
```

### Variáveis de Ambiente Necessárias

**Frontend (.env.local.example):**

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

**Backend (.env.example):**

```
# Database
DATABASE_URL=postgresql://dona:maria@postgres:5432/donamaria

# Redis
REDIS_URL=redis://redis:6379

# API Keys (para stories futuras)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
TAVILY_API_KEY=

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Theme/Design System

Cores definidas no UX Design para configurar no Tailwind:

- Base: `#333333`
- Primary: `#aeffde`
- Secondary: `#e4f1ff`
- Typography: Inter (primary), JetBrains Mono (code)

### Padrões de Código

**Frontend:**

- ESLint config: `next/core-web-vitals` + `@typescript-eslint/recommended`
- Prettier: `semi: true`, `singleQuote: true`, `tabWidth: 2`
- Import order: React → Next → External → Internal → Styles

**Backend:**

- Ruff: `select = ["E", "F", "I", "N", "W", "UP", "ANN", "B", "C4", "SIM"]`
- MyPy: `strict = true`, `disallow_untyped_defs = true`
- Docstrings: Google style

### Endpoints Iniciais do Backend

O `main.py` deve conter:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Dona-Maria-IA API",
    description="A honest AI that knows when it doesn't know",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dona-maria-ia"}

@app.get("/")
async def root():
    return {"message": "Dona Maria está aqui para ajudar!"}
```

### Project Structure Notes

- Frontend e Backend são projetos separados no mesmo repositório (monorepo)
- Docker Compose orquestra todos os serviços para desenvolvimento local
- Não implementar autenticação ou database migrations nesta story
- Foco é ter a estrutura base funcionando com hot reload

### Testing Requirements

- Validar que `docker-compose up` inicia sem erros
- Validar que frontend responde em http://localhost:3000
- Validar que Swagger UI abre em http://localhost:8000/docs
- Validar que health check retorna `{"status": "healthy"}`
- Validar que linters passam sem erros (ESLint, Ruff, MyPy)

### References

- [Source: architecture.md#Technology Stack] - Stack técnica completa
- [Source: architecture.md#Environment Configuration] - Docker Compose config
- [Source: prd.md#Product Scope] - MVP features scope
- [Source: ux-design-specification.md] - Theme colors e typography
- [Source: epics.md#Story 1.1] - Acceptance criteria originais

---

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (Amelia - Developer Agent)

### Debug Log References

- Ruff linting: All checks passed após correção de UP035 e ARG001
- Backend tests: 3/3 passed (test_health_check, test_root_endpoint, test_api_v1_status)
- TypeScript: tsc --noEmit passou sem erros
- Docker: Build e up bem sucedidos

### Completion Notes List

- ✅ Task 1: Estrutura base criada (frontend/, backend/, docker/, README.md, .gitignore)
- ✅ Task 2: Next.js 16.1.2 com TypeScript, Tailwind CSS 4, ESLint, Prettier configurados
- ✅ Task 3: FastAPI 0.128.0 com Pydantic 2.12.5, Ruff, MyPy, pytest configurados
- ✅ Task 4: Docker Compose com PostgreSQL 16, Redis 7, volumes e healthchecks
- ✅ Task 5: Validação completa - todos serviços funcionando:
  - Frontend: http://localhost:3000 → HTTP 200
  - Backend: http://localhost:8000/health → {"status": "healthy"}
  - Swagger: http://localhost:8000/docs → OK
  - PostgreSQL: accepting connections
  - Redis: PONG

### Change Log

| Data       | Mudança                                 | Razão                                     |
| ---------- | --------------------------------------- | ----------------------------------------- |
| 2026-01-15 | Criação da estrutura inicial do projeto | Story 1.1 - Setup Inicial                 |
| 2026-01-15 | Correção do Dockerfile.dev backend      | README.md necessário para hatchling build |
| 2026-01-15 | Adição de .dockerignore                 | Evitar copiar node_modules e cache        |

### File List

**Arquivos Criados:**

- `.gitignore` - Gitignore para monorepo Python + Node
- `README.md` - Documentação principal
- `.env.example` - Variáveis de ambiente de exemplo
- `docker-compose.yml` - Orquestração de serviços
- `frontend/Dockerfile.dev` - Imagem dev Next.js
- `frontend/.prettierrc` - Configuração Prettier
- `frontend/.env.local.example` - Envvars frontend
- `frontend/.dockerignore` - Ignore Docker frontend
- `frontend/src/lib/utils.ts` - Utilitários
- `frontend/src/lib/api.ts` - Cliente API
- `frontend/src/lib/index.ts` - Barrel export
- `frontend/src/hooks/index.ts` - Barrel export hooks
- `frontend/src/components/index.ts` - Barrel export components
- `backend/pyproject.toml` - Config Python/dependências
- `backend/ruff.toml` - Configuração Ruff linter
- `backend/README.md` - Documentação backend
- `backend/.env.example` - Envvars backend
- `backend/Dockerfile.dev` - Imagem dev FastAPI
- `backend/.dockerignore` - Ignore Docker backend
- `backend/app/__init__.py`
- `backend/app/main.py` - Entry point FastAPI
- `backend/app/config/__init__.py`
- `backend/app/config/settings.py` - Pydantic Settings
- `backend/app/api/__init__.py`
- `backend/app/api/v1/__init__.py`
- `backend/app/api/v1/router.py` - Router API v1
- `backend/app/models/__init__.py`
- `backend/app/services/__init__.py`
- `backend/app/schemas/__init__.py`
- `backend/tests/__init__.py`
- `backend/tests/test_main.py` - Testes dos endpoints
