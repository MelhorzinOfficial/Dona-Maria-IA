# Story 1.2: Registro de Usuário com Email

Status: done

## Story

As a **novo usuário**,
I want **criar uma conta usando meu email e senha**,
So that **possa ter acesso personalizado à Dona Maria**.

## Acceptance Criteria

1. **Given** um visitante na página de registro
   **When** ele preenche email válido e senha (mínimo 8 caracteres)
   **Then** uma nova conta é criada no banco de dados
   **And** a senha é armazenada com bcrypt (cost factor 12)
   **And** o usuário recebe um token JWT
   **And** o usuário é redirecionado para o chat

2. **Given** um email já registrado
   **When** tentativa de registro com mesmo email
   **Then** erro "Email já cadastrado" é exibido
   **And** nenhuma conta duplicada é criada

3. **Given** senha com menos de 8 caracteres
   **When** tentativa de registro
   **Then** erro de validação é exibido
   **And** registro não é permitido

## Tasks / Subtasks

- [x] **Task 1: Setup do Sistema de Autenticação Backend** (AC: #1)

  - [x] 1.1 Instalar dependências: `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`
  - [x] 1.2 Criar `backend/app/config/auth.py` com settings de JWT (SECRET_KEY, ALGORITHM, expire times)
  - [x] 1.3 Criar `backend/app/services/auth_service.py` com funções de hash/verify password e create/verify token

- [x] **Task 2: Database Models e Migrations** (AC: #1, #2)

  - [x] 2.1 Instalar `sqlalchemy[asyncio]`, `asyncpg`, `alembic`
  - [x] 2.2 Criar `backend/app/models/user.py` com modelo SQLAlchemy User
  - [x] 2.3 Configurar Alembic para migrations
  - [x] 2.4 Criar migration inicial com tabela `users`
  - [x] 2.5 Criar `backend/app/config/database.py` com async engine e session factory

- [x] **Task 3: Schemas Pydantic** (AC: #1, #2, #3)

  - [x] 3.1 Criar `backend/app/schemas/auth.py` com UserCreate, UserResponse, Token schemas
  - [x] 3.2 Implementar validação de email (EmailStr do Pydantic)
  - [x] 3.3 Implementar validação de senha (mínimo 8 caracteres)

- [x] **Task 4: API Endpoints de Registro** (AC: #1, #2, #3)

  - [x] 4.1 Criar `backend/app/api/v1/auth.py` com router de autenticação
  - [x] 4.2 Implementar endpoint `POST /api/v1/auth/register`
  - [x] 4.3 Implementar verificação de email duplicado (AC: #2)
  - [x] 4.4 Retornar JWT tokens no registro bem-sucedido
  - [ ] 4.5 Adicionar rate limiting no endpoint (60 req/min) ⚠️ _Pendente para próxima story_

- [x] **Task 5: Frontend - Página de Registro** (AC: #1, #2, #3)

  - [x] 5.1 Criar `frontend/src/app/(auth)/register/page.tsx`
  - [x] 5.2 Criar componente `RegisterForm` com campos email e senha
  - [x] 5.3 Implementar validação client-side (email válido, senha >= 8 chars)
  - [x] 5.4 Criar hook `useAuth` com função register
  - [x] 5.5 Implementar feedback visual de loading e erros
  - [x] 5.6 Implementar redirecionamento para `/chat` após sucesso

- [x] **Task 6: Testes** (AC: #1, #2, #3)
  - [x] 6.1 Criar testes backend para registro (pytest + httpx)
  - [x] 6.2 Testar criação de usuário com dados válidos
  - [x] 6.3 Testar rejeição de email duplicado
  - [x] 6.4 Testar rejeição de senha curta
  - [x] 6.5 Testar hash correto do bcrypt (cost factor 12)

## Dev Notes

### Dependências a Instalar

**Backend (adicionar ao pyproject.toml):**

```toml
[project.dependencies]
# Existentes...
sqlalchemy = {version = ">=2.0.0", extras = ["asyncio"]}
asyncpg = ">=0.29.0"
alembic = ">=1.13.0"
python-jose = {version = ">=3.3.0", extras = ["cryptography"]}
passlib = {version = ">=1.7.4", extras = ["bcrypt"]}
python-multipart = ">=0.0.6"
```

**Frontend (verificar se já existem):**

```json
{
	"dependencies": {
		"react-hook-form": "^7.x",
		"@hookform/resolvers": "^3.x",
		"zod": "^3.x"
	}
}
```

### Estrutura de Arquivos a Criar

```
backend/
├── app/
│   ├── config/
│   │   ├── auth.py          # JWT settings
│   │   └── database.py      # Async SQLAlchemy setup
│   ├── models/
│   │   ├── base.py          # SQLAlchemy Base
│   │   └── user.py          # User model
│   ├── schemas/
│   │   └── auth.py          # Pydantic schemas
│   ├── services/
│   │   └── auth_service.py  # Auth business logic
│   └── api/v1/
│       └── auth.py          # Auth router
├── alembic/
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
│       └── 001_create_users_table.py
└── tests/
    └── test_auth.py

frontend/
└── src/
    ├── app/
    │   └── (auth)/
    │       └── register/
    │           └── page.tsx
    ├── components/
    │   └── auth/
    │       └── RegisterForm.tsx
    └── hooks/
        └── useAuth.ts
```

### Schema do Banco de Dados (User)

Conforme [architecture.md#Database Schema]:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(100),
    avatar_url TEXT,
    auth_provider VARCHAR(50) DEFAULT 'email',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### Modelo SQLAlchemy

```python
# backend/app/models/user.py
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Null para OAuth
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String, nullable=True)
    auth_provider = Column(String(50), default="email")
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### Configuração JWT

Conforme [architecture.md#Security Measures]:

- **Algorithm:** RS256 (ou HS256 para simplicidade inicial)
- **Access Token:** 15 minutos
- **Refresh Token:** 7 dias
- **Password:** bcrypt com cost factor 12

```python
# backend/app/config/auth.py
from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    bcrypt_rounds: int = 12

    class Config:
        env_prefix = "AUTH_"
```

### Schemas Pydantic

```python
# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Senha com mínimo 8 caracteres")

class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: str | None = None
    auth_provider: str
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: UUID | None = None
```

### Endpoint de Registro

```python
# backend/app/api/v1/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService
from app.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registrar novo usuário com email e senha.

    - **email**: Email válido e único
    - **password**: Mínimo 8 caracteres
    """
    auth_service = AuthService(db)

    # Verificar se email já existe
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Criar usuário
    user = await auth_service.create_user(user_data)

    # Gerar tokens
    tokens = auth_service.create_tokens(user.id)

    return tokens
```

### Componente Frontend RegisterForm

```typescript
// frontend/src/components/auth/RegisterForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuth } from '@/hooks/useAuth';

const registerSchema = z
	.object({
		email: z.string().email('Email inválido'),
		password: z.string().min(8, 'Senha deve ter no mínimo 8 caracteres'),
		confirmPassword: z.string(),
	})
	.refine((data) => data.password === data.confirmPassword, {
		message: 'Senhas não conferem',
		path: ['confirmPassword'],
	});

type RegisterFormData = z.infer<typeof registerSchema>;

export function RegisterForm() {
	const { register: registerUser, isLoading, error } = useAuth();
	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm<RegisterFormData>({
		resolver: zodResolver(registerSchema),
	});

	const onSubmit = async (data: RegisterFormData) => {
		await registerUser({
			email: data.email,
			password: data.password,
		});
	};

	// ... render form
}
```

### Padrões de Código a Seguir

**Backend (conforme story 1-1):**

- Ruff: `select = ["E", "F", "I", "N", "W", "UP", "ANN", "B", "C4", "SIM"]`
- MyPy: strict mode
- Docstrings: Google style
- Async/await para todas operações de I/O

**Frontend (conforme story 1-1):**

- ESLint: next/core-web-vitals + @typescript-eslint/recommended
- Prettier: semi, singleQuote, tabWidth: 2
- Componentes com "use client" quando necessário
- Validação client-side com Zod

### Theme/Design System

Conforme [ux-design-specification.md]:

- Base: `#333333`
- Primary: `#aeffde`
- Secondary: `#e4f1ff`
- Error: `#ff8080`
- Font: Inter (form labels), JetBrains Mono (inputs de código)

### Tratamento de Erros

| Erro            | Código HTTP | Mensagem PT-BR                           |
| --------------- | ----------- | ---------------------------------------- |
| Email inválido  | 422         | "Email inválido"                         |
| Email duplicado | 400         | "Email já cadastrado"                    |
| Senha curta     | 422         | "Senha deve ter no mínimo 8 caracteres"  |
| Rate limit      | 429         | "Muitas tentativas. Aguarde um momento." |
| Erro servidor   | 500         | "Erro interno. Tente novamente."         |

### Segurança

Conforme [architecture.md#Security Measures]:

- ✅ Password hashing: bcrypt cost factor 12
- ✅ Input validation: Pydantic + Zod
- ✅ Rate limiting: 60 req/min por IP
- ✅ CORS: whitelist localhost:3000 (dev)
- ✅ SQL Injection: SQLAlchemy ORM

### Testing Requirements

**Backend Tests (pytest):**

```python
# tests/test_auth.py
import pytest
from httpx import AsyncClient
from passlib.hash import bcrypt

class TestRegister:
    async def test_register_success(self, client: AsyncClient):
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "password123"
        })
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        # Primeiro registro
        await client.post("/api/v1/auth/register", json={
            "email": "dupe@example.com",
            "password": "password123"
        })
        # Segunda tentativa
        response = await client.post("/api/v1/auth/register", json={
            "email": "dupe@example.com",
            "password": "password456"
        })
        assert response.status_code == 400
        assert "já cadastrado" in response.json()["detail"]

    async def test_register_short_password(self, client: AsyncClient):
        response = await client.post("/api/v1/auth/register", json={
            "email": "short@example.com",
            "password": "123"
        })
        assert response.status_code == 422

    async def test_password_is_hashed_with_bcrypt(self, db_session):
        # Verificar que bcrypt cost factor é 12
        user = await get_user_by_email(db_session, "test@example.com")
        assert user.password_hash.startswith("$2b$12$")
```

### Project Structure Notes

- Esta é a primeira story que implementa banco de dados
- Alembic será usado para gerenciar migrations (permite rollback)
- Async SQLAlchemy 2.0 style (usando `async_sessionmaker`)
- JWT armazenado no frontend via localStorage (ou httpOnly cookies para prod)
- Refresh token permite sessão persistente sem re-login

### Previous Story Intelligence

**Da Story 1.1 (Setup Inicial):**

- Docker Compose já configurado com PostgreSQL e Redis
- DATABASE_URL: `postgresql://dona:maria@postgres:5432/donamaria`
- Backend estrutura já existe em `backend/app/`
- `main.py` já tem FastAPI app com CORS configurado
- Settings já usa Pydantic BaseSettings
- Hot reload funcionando com Uvicorn

**Arquivos existentes relevantes:**

- [backend/app/main.py](backend/app/main.py) - App FastAPI base
- [backend/app/config/settings.py](backend/app/config/settings.py) - Settings existentes
- [backend/app/api/v1/router.py](backend/app/api/v1/router.py) - Router v1 existente

### References

- [Source: architecture.md#Database Schema] - Schema completo da tabela users
- [Source: architecture.md#Security Architecture] - Fluxo de autenticação
- [Source: architecture.md#Security Measures] - bcrypt cost factor 12, JWT specs
- [Source: epics.md#Story 1.2] - Acceptance criteria originais
- [Source: prd.md#FR1] - Requisito funcional de registro
- [Source: ux-design-specification.md] - Theme colors

---

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (GitHub Copilot)

### Debug Log References

1. **SQLite in-memory table sharing issue**: Testes falhavam com "no such table: users" - resolvido trocando NullPool por StaticPool com `connect_args={"check_same_thread": False}`
2. **passlib/bcrypt incompatibilidade Python 3.14**: passlib não suporta bcrypt 4.x corretamente - resolvido usando bcrypt diretamente em vez de passlib.CryptContext
3. **email-validator missing**: Pydantic EmailStr requer `pydantic[email]` - corrigido no pyproject.toml

### Completion Notes List

- ✅ Todos os 3 Acceptance Criteria atendidos
- ✅ 14/14 testes passando (11 auth + 3 main)
- ✅ Backend: autenticação JWT com bcrypt (cost factor 12)
- ✅ Frontend: formulário de registro com validação Zod
- ✅ [CR] Router de autenticação registrado corretamente
- ✅ [CR] Dependências bcrypt e python-jose adicionadas
- ✅ [CR] Tratamento de erro melhorado no frontend
- ⚠️ **Rate limiting (Task 4.5) não implementado** - requer adicionar middleware/decorator separadamente
- ⚠️ **localStorage para tokens** - considerar httpOnly cookies em produção

### Change Log

| Data       | Mudança                                | Razão                                     |
| ---------- | -------------------------------------- | ----------------------------------------- |
| 2026-01-15 | Story criada                           | Create-story workflow                     |
| 2026-01-15 | Implementação completa                 | Dev-story workflow                        |
| 2026-01-15 | Migração passlib → bcrypt direto       | Incompatibilidade Python 3.14             |
| 2026-01-15 | [CR] auth_router incluído no router.py | Code Review: router não estava registrado |
| 2026-01-15 | [CR] bcrypt + python-jose adicionados  | Code Review: dependências faltando        |
| 2026-01-15 | [CR] Tratamento erro JSON no useAuth   | Code Review: falha silenciosa em erros    |

### File List

**Arquivos Criados:**

- `backend/app/config/auth.py` - Configurações JWT e bcrypt
- `backend/app/config/database.py` - SQLAlchemy async engine
- `backend/app/models/base.py` - DeclarativeBase SQLAlchemy
- `backend/app/models/user.py` - Modelo User
- `backend/app/schemas/auth.py` - Schemas Pydantic (UserCreate, UserResponse, Token, TokenData)
- `backend/app/services/auth_service.py` - AuthService com hash/verify password e JWT
- `backend/app/api/v1/auth.py` - Router /api/v1/auth com endpoint /register
- `backend/alembic.ini` - Configuração Alembic
- `backend/alembic/env.py` - Alembic environment async
- `backend/alembic/script.py.mako` - Template de migrations
- `backend/alembic/versions/001_create_users_table.py` - Migration inicial
- `backend/tests/conftest.py` - Fixtures pytest com SQLite in-memory
- `backend/tests/test_auth.py` - 11 testes de registro
- `frontend/src/hooks/useAuth.ts` - Hook de autenticação
- `frontend/src/components/auth/RegisterForm.tsx` - Componente de registro
- `frontend/src/app/(auth)/register/page.tsx` - Página de registro

**Arquivos Modificados:**

- `backend/pyproject.toml` - Dependências: bcrypt, python-jose, sqlalchemy, asyncpg, alembic, aiosqlite, pydantic[email]
- `backend/app/api/v1/router.py` - Include auth_router
- `frontend/package.json` - Dependências: react-hook-form, @hookform/resolvers, zod
