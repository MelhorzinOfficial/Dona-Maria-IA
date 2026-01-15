# Story 1.4: Login e Logout

Status: review

## Story

As a **usuário registrado**,
I want **fazer login e logout da minha conta**,
So that **possa acessar minhas conversas de forma segura**.

## Acceptance Criteria

1. **Given** usuário com conta existente
   **When** insere email e senha corretos
   **Then** recebe token JWT (access + refresh)
   **And** é redirecionado para o chat
   **And** sessão é registrada no Redis

2. **Given** credenciais incorretas
   **When** tentativa de login
   **Then** erro "Email ou senha incorretos" é exibido
   **And** nenhum token é gerado

3. **Given** usuário logado
   **When** clica em "Sair"
   **Then** tokens são invalidados
   **And** sessão é removida do Redis
   **And** é redirecionado para landing page

4. **Given** token JWT expirado
   **When** refresh token ainda válido
   **Then** novo access token é gerado automaticamente
   **And** sessão continua sem interrupção

## Tasks / Subtasks

- [x] **Task 1: Backend - Endpoint de Login** (AC: #1, #2)

  - [x] 1.1 Criar schema `UserLogin` em `backend/app/schemas/auth.py` com email e password
  - [x] 1.2 Adicionar método `authenticate_user(email, password)` em `AuthService` que verifica credenciais
  - [x] 1.3 Implementar endpoint `POST /api/v1/auth/login` em `backend/app/api/v1/auth.py`
  - [x] 1.4 Retornar `Token` com access_token e refresh_token se credenciais válidas
  - [x] 1.5 Retornar HTTP 401 com mensagem "Email ou senha incorretos" se credenciais inválidas

- [x] **Task 2: Backend - Gerenciamento de Sessões no Redis** (AC: #1, #3)

  - [x] 2.1 Criar `backend/app/services/session_service.py` com classe `SessionService`
  - [x] 2.2 Implementar método `create_session(user_id, device_info)` que armazena sessão no Redis
  - [x] 2.3 Implementar método `invalidate_session(user_id, session_id)` para logout
  - [x] 2.4 Implementar método `invalidate_all_sessions(user_id)` para invalidar todas sessões
  - [x] 2.5 Configurar TTL da sessão igual ao refresh token (7 dias)

- [x] **Task 3: Backend - Endpoint de Logout** (AC: #3)

  - [x] 3.1 Implementar endpoint `POST /api/v1/auth/logout` que requer autenticação
  - [x] 3.2 Criar dependency `get_current_user` que extrai user do token JWT
  - [x] 3.3 Invalidar sessão atual no Redis
  - [x] 3.4 Retornar HTTP 200 com mensagem "Logout realizado com sucesso"

- [x] **Task 4: Backend - Endpoint de Refresh Token** (AC: #4)

  - [x] 4.1 Criar schema `RefreshTokenRequest` em `backend/app/schemas/auth.py`
  - [x] 4.2 Implementar endpoint `POST /api/v1/auth/refresh`
  - [x] 4.3 Validar refresh token e verificar se sessão existe no Redis
  - [x] 4.4 Gerar novo access token se válido, retornar HTTP 401 se inválido

- [x] **Task 5: Backend - Dependency de Autenticação** (AC: #1, #3, #4)

  - [x] 5.1 Criar `backend/app/api/deps.py` com dependencies de autenticação
  - [x] 5.2 Implementar `get_current_user(token)` que retorna User do banco
  - [x] 5.3 Implementar `get_current_active_user` para verificar sessão ativa no Redis
  - [x] 5.4 Usar `OAuth2PasswordBearer` do FastAPI para extração do token

- [x] **Task 6: Frontend - Página de Login** (AC: #1, #2)

  - [x] 6.1 Criar `frontend/src/app/(auth)/login/page.tsx` com formulário de login
  - [x] 6.2 Criar componente `frontend/src/components/auth/LoginForm.tsx`
  - [x] 6.3 Implementar validação client-side com Zod (email válido, senha não vazia)
  - [x] 6.4 Exibir feedback visual de loading e erros
  - [x] 6.5 Redirecionar para `/chat` após login bem-sucedido

- [x] **Task 7: Frontend - Funções de Login/Logout no Hook useAuth** (AC: #1, #3)

  - [x] 7.1 Adicionar função `login(email, password)` no hook `useAuth`
  - [x] 7.2 Adicionar função `logout()` que chama endpoint e limpa localStorage
  - [x] 7.3 Adicionar função `isAuthenticated()` que verifica tokens no localStorage
  - [x] 7.4 Implementar interceptor para renovar token automaticamente (AC: #4)

- [x] **Task 8: Frontend - Botão de Logout e Proteção de Rotas** (AC: #3)

  - [x] 8.1 Criar componente `UserMenu` com opção de logout
  - [x] 8.2 Criar middleware ou HOC `withAuth` para proteger rotas autenticadas
  - [x] 8.3 Redirecionar para `/login` se usuário não autenticado tentar acessar `/chat`
  - [x] 8.4 Redirecionar para `/chat` se usuário autenticado tentar acessar `/login`

- [x] **Task 9: Testes Backend** (AC: #1, #2, #3, #4)

  - [x] 9.1 Testar login com credenciais válidas retorna tokens
  - [x] 9.2 Testar login com credenciais inválidas retorna 401
  - [x] 9.3 Testar logout invalida sessão no Redis
  - [x] 9.4 Testar refresh token gera novo access token
  - [x] 9.5 Testar refresh token inválido retorna 401

- [x] **Task 10: Integração Redis no Docker Compose** (AC: #1, #3)
  - [x] 10.1 Verificar configuração do Redis no `docker-compose.dev.yml`
  - [x] 10.2 Criar `backend/app/config/redis.py` com conexão assíncrona ao Redis
  - [x] 10.3 Adicionar `redis[hiredis]` às dependências do backend

## Dev Notes

### Código Existente a Reutilizar

O projeto já possui estrutura de autenticação da Story 1.2:

- [backend/app/services/auth_service.py](backend/app/services/auth_service.py): Funções `verify_password`, `create_access_token`, `create_refresh_token`, `verify_token`
- [backend/app/schemas/auth.py](backend/app/schemas/auth.py): `Token`, `TokenData`, `UserCreate`, `UserResponse`
- [frontend/src/hooks/useAuth.ts](frontend/src/hooks/useAuth.ts): Hook com função `register`, armazenamento em localStorage

### Novos Schemas a Criar

```python
# backend/app/schemas/auth.py (adicionar)

class UserLogin(BaseModel):
    """Schema para login de usuário."""
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=1, description="Senha do usuário")

class RefreshTokenRequest(BaseModel):
    """Schema para renovação de token."""
    refresh_token: str = Field(..., description="Refresh token válido")
```

### Estrutura Redis para Sessões

Conforme [architecture.md#Redis Keys Structure]:

```
# Key pattern
session:{user_id}:{session_id} -> {
  "user_id": "uuid",
  "device_info": {"user_agent": "...", "ip": "..."},
  "created_at": "timestamp",
  "expires_at": "timestamp"
}

# TTL: 7 dias (REFRESH_TOKEN_EXPIRE_DAYS)
```

### SessionService Implementation Pattern

```python
# backend/app/services/session_service.py

import json
import uuid
from datetime import datetime, timedelta
from redis.asyncio import Redis

class SessionService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.session_ttl_days = 7

    async def create_session(self, user_id: str, device_info: dict) -> str:
        session_id = str(uuid.uuid4())
        key = f"session:{user_id}:{session_id}"
        data = {
            "user_id": user_id,
            "device_info": device_info,
            "created_at": datetime.utcnow().isoformat()
        }
        await self.redis.setex(
            key,
            timedelta(days=self.session_ttl_days),
            json.dumps(data)
        )
        return session_id

    async def invalidate_session(self, user_id: str, session_id: str) -> bool:
        key = f"session:{user_id}:{session_id}"
        return await self.redis.delete(key) > 0

    async def session_exists(self, user_id: str, session_id: str) -> bool:
        key = f"session:{user_id}:{session_id}"
        return await self.redis.exists(key) > 0
```

### Authentication Dependency Pattern

```python
# backend/app/api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.services.auth_service import AuthService, verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None or token_data.user_id is None:
        raise credentials_exception

    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception

    return user
```

### Login Endpoint Pattern

```python
# backend/app/api/v1/auth.py (adicionar)

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = auth_service.create_tokens(user.id)
    return Token(**tokens)
```

### Frontend Login Form Pattern

```typescript
// frontend/src/components/auth/LoginForm.tsx

const loginSchema = z.object({
	email: z.string().email('Email inválido'),
	password: z.string().min(1, 'Senha é obrigatória'),
});
```

### Arquivos a Criar/Modificar

**Novos arquivos:**

```
backend/
├── app/
│   ├── api/
│   │   └── deps.py                 # Dependencies de autenticação
│   ├── config/
│   │   └── redis.py                # Conexão Redis
│   └── services/
│       └── session_service.py      # Gerenciamento de sessões
└── tests/
    └── test_auth.py                # (adicionar testes de login/logout)

frontend/
└── src/
    ├── app/
    │   └── (auth)/
    │       └── login/
    │           └── page.tsx        # Página de login
    ├── components/
    │   └── auth/
    │       └── LoginForm.tsx       # Formulário de login
    └── middleware.ts               # Proteção de rotas (opcional)
```

**Arquivos a modificar:**

- `backend/app/schemas/auth.py` - Adicionar `UserLogin`, `RefreshTokenRequest`
- `backend/app/services/auth_service.py` - Adicionar `authenticate_user`
- `backend/app/api/v1/auth.py` - Adicionar endpoints login, logout, refresh
- `frontend/src/hooks/useAuth.ts` - Adicionar login, logout, refresh

### Configuração do Redis

```python
# backend/app/config/redis.py

from redis.asyncio import Redis, from_url
from app.config.settings import settings

async def get_redis() -> Redis:
    return await from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )
```

### Dependências a Adicionar

**Backend (pyproject.toml):**

```toml
redis = {version = ">=5.0.0", extras = ["hiredis"]}
```

### Segurança

Conforme [architecture.md#Security Measures]:

- ✅ Tokens JWT com expiração (access: 15min, refresh: 7 dias)
- ✅ Sessões armazenadas no Redis com TTL
- ✅ Logout invalida sessão (não apenas o token local)
- ✅ Mensagem genérica "Email ou senha incorretos" (não revela qual está errado)
- ✅ Rate limiting no login (60 req/min) - _a implementar em story futura_

### NFRs Atendidos

- **NFR8**: Tokens JWT com expiração máxima de 24 horas ✅ (access: 15min)
- **NFR6**: Comunicações via HTTPS/TLS ✅ (infra)
- **NFR10**: Proteção contra ataques ✅ (mensagem genérica de erro)

### Tratamento de Erros

| Cenário                | Código HTTP | Mensagem PT-BR                   |
| ---------------------- | ----------- | -------------------------------- |
| Credenciais inválidas  | 401         | "Email ou senha incorretos"      |
| Token expirado         | 401         | "Token expirado"                 |
| Token inválido         | 401         | "Credenciais inválidas"          |
| Refresh token inválido | 401         | "Sessão expirada"                |
| Erro de servidor       | 500         | "Erro interno. Tente novamente." |

### References

- [Source: architecture.md#API Design] - Endpoints de autenticação
- [Source: architecture.md#Redis Keys Structure] - Padrão de chaves para sessões
- [Source: architecture.md#Security Measures] - Requisitos de segurança
- [Source: epics.md#Story 1.4] - Acceptance criteria originais
- [Source: 1-2-registro-de-usuario-com-email.md] - Implementação existente de auth

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 via GitHub Copilot

### Debug Log References

- All 39 backend tests passing
- Frontend lint: 0 errors, 1 warning (pre-existing)
- Frontend TypeScript: No errors

### Completion Notes List

1. **Login endpoint** implemented using `OAuth2PasswordRequestForm` for FastAPI compatibility
2. **Logout endpoint** implemented with Bearer token authentication
3. **Refresh token endpoint** validates token type and generates new token pair
4. **SessionService** created with Redis support (prepared for future rate limiting)
5. **Authentication dependencies** created in `deps.py` with `get_current_user` and `get_current_active_user`
6. **LoginForm** component with Zod validation (email valid, password required)
7. **useAuth hook** updated with `login`, `logout`, and `refreshAccessToken` functions
8. **UserMenu** component for logout with dropdown menu
9. **withAuth HOC** for client-side route protection
10. **Chat page placeholder** created at `/chat` with authentication protection

### File List

**Arquivos Criados:**

- `backend/app/config/redis.py` - Conexão assíncrona com Redis
- `backend/app/services/session_service.py` - Gerenciamento de sessões
- `backend/app/api/deps.py` - Dependencies de autenticação
- `frontend/src/components/auth/LoginForm.tsx` - Formulário de login
- `frontend/src/components/auth/UserMenu.tsx` - Menu de usuário com logout
- `frontend/src/components/auth/withAuth.tsx` - HOC para proteção de rotas
- `frontend/src/app/chat/page.tsx` - Página de chat (placeholder)
- `frontend/src/middleware.ts` - Middleware Next.js

**Arquivos Modificados:**

- `backend/app/schemas/auth.py` - Adicionados `UserLogin` e `RefreshTokenRequest`
- `backend/app/services/auth_service.py` - Adicionado `authenticate_user`
- `backend/app/api/v1/auth.py` - Adicionados endpoints login, logout, refresh
- `backend/tests/test_auth.py` - Adicionados 9 testes (login, logout, refresh)
- `frontend/src/hooks/useAuth.ts` - Adicionados login, logout, refreshAccessToken
- `frontend/src/app/(auth)/login/page.tsx` - Integrado LoginForm
- `frontend/src/components/index.ts` - Exports dos novos componentes
