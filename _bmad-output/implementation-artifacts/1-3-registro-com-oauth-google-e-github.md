# Story 1.3: Registro com OAuth (Google e GitHub)

Status: review

## Story

As a **novo usuário**,
I want **criar conta usando minha conta Google ou GitHub**,
So that **possa me registrar rapidamente sem criar nova senha**.

## Acceptance Criteria

1. **Given** um visitante na página de registro/login
   **When** ele clica em "Continuar com Google"
   **Then** é redirecionado para OAuth do Google
   **And** após autorização, conta é criada (se nova) ou vinculada (se existe)
   **And** recebe token JWT (access + refresh)
   **And** é redirecionado ao chat

2. **Given** um visitante na página de registro/login
   **When** ele clica em "Continuar com GitHub"
   **Then** é redirecionado para OAuth do GitHub
   **And** após autorização, conta é criada (se nova) ou vinculada (se existe)
   **And** recebe token JWT (access + refresh)
   **And** é redirecionado ao chat

3. **Given** email do OAuth já existe como conta local (email/password)
   **When** login via OAuth
   **Then** contas são vinculadas automaticamente
   **And** usuário pode usar ambos os métodos (email ou OAuth)
   **And** `auth_provider` no banco não é sobrescrito (mantém histórico)

4. **Given** usuário OAuth tenta logout
   **When** sessão é encerrada
   **Then** tokens são invalidados no Redis
   **And** usuário precisa re-autorizar OAuth no próximo login

5. **Given** provedor OAuth está indisponível ou usuário cancela
   **When** callback retorna erro
   **Then** erro amigável é exibido na página de login
   **And** nenhuma conta é criada/modificada

## Tasks / Subtasks

- [x] **Task 1: Configuração OAuth Backend** (AC: #1, #2)

  - [x] 1.1 Instalar dependência `authlib>=1.3.0` no pyproject.toml
  - [x] 1.2 Criar `backend/app/config/oauth.py` com settings para Google e GitHub
  - [x] 1.3 Configurar OAuth clients com client_id, client_secret, scopes
  - [x] 1.4 Definir redirect URIs para desenvolvimento e produção

- [x] **Task 2: Serviço OAuth** (AC: #1, #2, #3)

  - [x] 2.1 Criar `backend/app/services/oauth_service.py`
  - [x] 2.2 Implementar `get_oauth_url(provider)` - gera URL de autorização
  - [x] 2.3 Implementar `handle_oauth_callback(provider, code)` - troca code por tokens
  - [x] 2.4 Implementar `get_user_info(provider, token)` - busca dados do usuário
  - [x] 2.5 Implementar lógica de criação/vinculação de conta com tratamento de email existente

- [x] **Task 3: Endpoints OAuth** (AC: #1, #2, #4, #5)

  - [x] 3.1 Criar endpoint `GET /api/v1/auth/oauth/{provider}` - inicia fluxo OAuth
  - [x] 3.2 Criar endpoint `GET /api/v1/auth/oauth/{provider}/callback` - recebe callback
  - [x] 3.3 Implementar validação de `state` para prevenir CSRF
  - [x] 3.4 Retornar JWT tokens no callback bem-sucedido
  - [x] 3.5 Implementar tratamento de erros do provedor

- [x] **Task 4: Schemas e Tipos** (AC: #1, #2)

  - [x] 4.1 Adicionar `OAuthProvider` enum em `backend/app/schemas/auth.py`
  - [x] 4.2 Criar `OAuthUserInfo` schema para dados do provedor
  - [x] 4.3 Criar `OAuthCallback` schema para resposta do callback

- [x] **Task 5: Frontend - Botões OAuth** (AC: #1, #2, #5)

  - [x] 5.1 Criar componente `frontend/src/components/auth/OAuthButtons.tsx`
  - [x] 5.2 Implementar botão "Continuar com Google" com ícone SVG
  - [x] 5.3 Implementar botão "Continuar com GitHub" com ícone SVG
  - [x] 5.4 Adicionar loading state durante redirecionamento
  - [x] 5.5 Integrar botões na página de registro `/register` existente
  - [x] 5.6 Integrar botões na página de login `/login` (se existir) ou criar

- [x] **Task 6: Frontend - Callback Handler** (AC: #1, #2, #5)

  - [x] 6.1 Criar `frontend/src/app/(auth)/oauth/callback/page.tsx`
  - [x] 6.2 Implementar processamento de query params (code, state, error)
  - [x] 6.3 Chamar API backend para trocar code por tokens
  - [x] 6.4 Armazenar tokens e redirecionar para `/chat`
  - [x] 6.5 Exibir erro amigável se OAuth falhar

- [x] **Task 7: Atualização do useAuth Hook** (AC: #1, #2, #3, #4)

  - [x] 7.1 Adicionar função `loginWithOAuth(provider)` no hook `useAuth`
  - [x] 7.2 Implementar redirecionamento para URL OAuth do backend
  - [x] 7.3 Atualizar função de logout para funcionar com OAuth users

- [x] **Task 8: Testes Backend** (AC: #1, #2, #3, #4, #5)
  - [x] 8.1 Criar `backend/tests/test_oauth.py`
  - [x] 8.2 Testar geração de URL OAuth (Google e GitHub)
  - [x] 8.3 Testar callback com mock de provedor
  - [x] 8.4 Testar criação de novo usuário via OAuth
  - [x] 8.5 Testar vinculação com conta existente (mesmo email)
  - [x] 8.6 Testar tratamento de erros (provedor indisponível, usuário cancela)

## Dev Notes

### Dependências a Instalar

**Backend (adicionar ao pyproject.toml):**

```toml
[project.dependencies]
# Existentes do 1.2...
authlib = ">=1.3.0"
httpx = ">=0.27.0"  # Para chamadas HTTP async ao provedor
```

### Estrutura de Arquivos a Criar/Modificar

```
backend/
├── app/
│   ├── config/
│   │   ├── auth.py          # Existente - adicionar OAuth settings
│   │   └── oauth.py         # NOVO - configuração específica OAuth
│   ├── schemas/
│   │   └── auth.py          # Modificar - adicionar OAuthProvider, OAuthUserInfo
│   ├── services/
│   │   ├── auth_service.py  # Existente - adicionar get_or_create_oauth_user
│   │   └── oauth_service.py # NOVO - lógica OAuth
│   └── api/v1/
│       └── auth.py          # Modificar - adicionar endpoints OAuth
└── tests/
    └── test_oauth.py        # NOVO - testes OAuth

frontend/
└── src/
    ├── app/
    │   └── (auth)/
    │       ├── register/
    │       │   └── page.tsx      # Modificar - adicionar OAuthButtons
    │       ├── login/
    │       │   └── page.tsx      # Criar se não existir
    │       └── oauth/
    │           └── callback/
    │               └── page.tsx  # NOVO - handler de callback
    ├── components/
    │   └── auth/
    │       ├── RegisterForm.tsx  # Existente
    │       └── OAuthButtons.tsx  # NOVO
    └── hooks/
        └── useAuth.ts            # Modificar - adicionar loginWithOAuth
```

### Configuração OAuth

**Google OAuth:**

- Console: https://console.cloud.google.com/apis/credentials
- Scopes necessários: `openid`, `email`, `profile`
- Redirect URI: `http://localhost:8000/api/v1/auth/oauth/google/callback` (dev)

**GitHub OAuth:**

- Console: https://github.com/settings/developers
- Scopes necessários: `read:user`, `user:email`
- Redirect URI: `http://localhost:8000/api/v1/auth/oauth/github/callback` (dev)

### Variáveis de Ambiente Necessárias

```env
# .env.example - adicionar
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# URLs de callback
OAUTH_REDIRECT_BASE=http://localhost:8000  # Mudar em produção
FRONTEND_URL=http://localhost:3000         # Para redirect final
```

### Configuração OAuth Backend

```python
# backend/app/config/oauth.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class OAuthSettings(BaseSettings):
    # Google
    google_client_id: str = ""
    google_client_secret: str = ""
    google_authorize_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_userinfo_url: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_scopes: list[str] = ["openid", "email", "profile"]

    # GitHub
    github_client_id: str = ""
    github_client_secret: str = ""
    github_authorize_url: str = "https://github.com/login/oauth/authorize"
    github_token_url: str = "https://github.com/login/oauth/access_token"
    github_userinfo_url: str = "https://api.github.com/user"
    github_emails_url: str = "https://api.github.com/user/emails"
    github_scopes: list[str] = ["read:user", "user:email"]

    # General
    oauth_redirect_base: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    state_secret: str = "change-me-in-production"  # Para gerar/validar state

    class Config:
        env_prefix = ""
        case_sensitive = False

@lru_cache
def get_oauth_settings() -> OAuthSettings:
    return OAuthSettings()

oauth_settings = get_oauth_settings()
```

### Serviço OAuth

```python
# backend/app/services/oauth_service.py
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Literal
from urllib.parse import urlencode

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.oauth import oauth_settings
from app.models.user import User
from app.schemas.auth import OAuthUserInfo, OAuthProvider

OAuthProviderType = Literal["google", "github"]

class OAuthService:
    """Serviço para autenticação OAuth."""

    def __init__(self):
        self._state_cache: dict[str, datetime] = {}  # Em produção, usar Redis

    def generate_oauth_url(self, provider: OAuthProviderType) -> tuple[str, str]:
        """
        Gera URL de autorização OAuth e state token.

        Returns:
            Tuple de (authorize_url, state)
        """
        state = secrets.token_urlsafe(32)
        self._state_cache[state] = datetime.now()

        if provider == "google":
            params = {
                "client_id": oauth_settings.google_client_id,
                "redirect_uri": f"{oauth_settings.oauth_redirect_base}/api/v1/auth/oauth/google/callback",
                "response_type": "code",
                "scope": " ".join(oauth_settings.google_scopes),
                "state": state,
                "access_type": "offline",
                "prompt": "consent",
            }
            return f"{oauth_settings.google_authorize_url}?{urlencode(params)}", state

        elif provider == "github":
            params = {
                "client_id": oauth_settings.github_client_id,
                "redirect_uri": f"{oauth_settings.oauth_redirect_base}/api/v1/auth/oauth/github/callback",
                "scope": " ".join(oauth_settings.github_scopes),
                "state": state,
            }
            return f"{oauth_settings.github_authorize_url}?{urlencode(params)}", state

        raise ValueError(f"Provider não suportado: {provider}")

    def validate_state(self, state: str) -> bool:
        """Valida state token para prevenir CSRF."""
        if state not in self._state_cache:
            return False

        created_at = self._state_cache.pop(state)
        # State válido por 10 minutos
        return datetime.now() - created_at < timedelta(minutes=10)

    async def exchange_code_for_token(
        self, provider: OAuthProviderType, code: str
    ) -> str:
        """Troca authorization code por access token."""
        async with httpx.AsyncClient() as client:
            if provider == "google":
                response = await client.post(
                    oauth_settings.google_token_url,
                    data={
                        "client_id": oauth_settings.google_client_id,
                        "client_secret": oauth_settings.google_client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": f"{oauth_settings.oauth_redirect_base}/api/v1/auth/oauth/google/callback",
                    },
                )
            elif provider == "github":
                response = await client.post(
                    oauth_settings.github_token_url,
                    data={
                        "client_id": oauth_settings.github_client_id,
                        "client_secret": oauth_settings.github_client_secret,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
            else:
                raise ValueError(f"Provider não suportado: {provider}")

            response.raise_for_status()
            data = response.json()
            return data["access_token"]

    async def get_user_info(
        self, provider: OAuthProviderType, access_token: str
    ) -> OAuthUserInfo:
        """Busca informações do usuário do provedor OAuth."""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}

            if provider == "google":
                response = await client.get(
                    oauth_settings.google_userinfo_url, headers=headers
                )
                response.raise_for_status()
                data = response.json()
                return OAuthUserInfo(
                    provider=OAuthProvider.GOOGLE,
                    provider_user_id=data["sub"],
                    email=data["email"],
                    name=data.get("name"),
                    avatar_url=data.get("picture"),
                )

            elif provider == "github":
                # GitHub precisa de duas chamadas: user info + emails
                response = await client.get(
                    oauth_settings.github_userinfo_url, headers=headers
                )
                response.raise_for_status()
                user_data = response.json()

                # Buscar email primário
                emails_response = await client.get(
                    oauth_settings.github_emails_url, headers=headers
                )
                emails_response.raise_for_status()
                emails = emails_response.json()
                primary_email = next(
                    (e["email"] for e in emails if e["primary"]), None
                )

                return OAuthUserInfo(
                    provider=OAuthProvider.GITHUB,
                    provider_user_id=str(user_data["id"]),
                    email=primary_email or user_data.get("email"),
                    name=user_data.get("name") or user_data.get("login"),
                    avatar_url=user_data.get("avatar_url"),
                )

            raise ValueError(f"Provider não suportado: {provider}")

    async def get_or_create_user(
        self, db: AsyncSession, user_info: OAuthUserInfo
    ) -> User:
        """
        Busca usuário existente ou cria novo.
        Vincula automaticamente se email já existe.
        """
        # Buscar por email existente
        result = await db.execute(
            select(User).where(User.email == user_info.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            # Atualizar avatar se não tiver
            if not existing_user.avatar_url and user_info.avatar_url:
                existing_user.avatar_url = user_info.avatar_url
            if not existing_user.display_name and user_info.name:
                existing_user.display_name = user_info.name
            await db.commit()
            return existing_user

        # Criar novo usuário
        new_user = User(
            email=user_info.email,
            display_name=user_info.name,
            avatar_url=user_info.avatar_url,
            auth_provider=user_info.provider.value,
            password_hash=None,  # OAuth users não têm senha
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
```

### Schemas OAuth

```python
# backend/app/schemas/auth.py - ADICIONAR

from enum import Enum

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"

class OAuthUserInfo(BaseModel):
    """Informações do usuário retornadas pelo provedor OAuth."""
    provider: OAuthProvider
    provider_user_id: str
    email: str
    name: str | None = None
    avatar_url: str | None = None

class OAuthCallbackResponse(BaseModel):
    """Resposta do callback OAuth."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
```

### Endpoints OAuth

```python
# backend/app/api/v1/auth.py - ADICIONAR aos endpoints existentes

from fastapi import Query
from fastapi.responses import RedirectResponse
from app.services.oauth_service import OAuthService
from app.schemas.auth import OAuthProvider, OAuthCallbackResponse

oauth_service = OAuthService()

@router.get("/oauth/{provider}")
async def oauth_redirect(provider: OAuthProvider):
    """
    Inicia fluxo OAuth redirecionando para o provedor.
    """
    authorize_url, state = oauth_service.generate_oauth_url(provider.value)
    # Em produção, state deveria ser armazenado em Redis
    response = RedirectResponse(url=authorize_url)
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        secure=True,  # True em produção
        max_age=600,  # 10 minutos
        samesite="lax",
    )
    return response

@router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: OAuthProvider,
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Callback do provedor OAuth.
    Troca code por token e cria/vincula usuário.
    """
    from app.config.oauth import oauth_settings

    # Verificar erro do provedor
    if error:
        error_url = f"{oauth_settings.frontend_url}/login?error={error}"
        return RedirectResponse(url=error_url)

    # Validar state (CSRF protection)
    if not oauth_service.validate_state(state):
        error_url = f"{oauth_settings.frontend_url}/login?error=invalid_state"
        return RedirectResponse(url=error_url)

    try:
        # Trocar code por access token
        access_token = await oauth_service.exchange_code_for_token(
            provider.value, code
        )

        # Buscar info do usuário
        user_info = await oauth_service.get_user_info(provider.value, access_token)

        # Criar ou vincular usuário
        user = await oauth_service.get_or_create_user(db, user_info)

        # Gerar JWT tokens
        from app.services.auth_service import create_access_token, create_refresh_token

        jwt_access = create_access_token(user.id)
        jwt_refresh = create_refresh_token(user.id)

        # Redirecionar para frontend com tokens
        # Em produção, usar httpOnly cookies ou outro método seguro
        callback_url = (
            f"{oauth_settings.frontend_url}/oauth/callback"
            f"?access_token={jwt_access}"
            f"&refresh_token={jwt_refresh}"
        )
        return RedirectResponse(url=callback_url)

    except Exception as e:
        error_url = f"{oauth_settings.frontend_url}/login?error=oauth_failed"
        return RedirectResponse(url=error_url)
```

### Frontend - OAuthButtons Component

```tsx
// frontend/src/components/auth/OAuthButtons.tsx
'use client';

import { useState } from 'react';

interface OAuthButtonsProps {
	onError?: (error: string) => void;
}

export function OAuthButtons({ onError }: OAuthButtonsProps) {
	const [loading, setLoading] = useState<'google' | 'github' | null>(null);

	const handleOAuth = (provider: 'google' | 'github') => {
		setLoading(provider);
		// Redirecionar para backend OAuth
		window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/oauth/${provider}`;
	};

	return (
		<div className="space-y-3">
			<button
				type="button"
				onClick={() => handleOAuth('google')}
				disabled={loading !== null}
				className="w-full flex items-center justify-center gap-3 px-4 py-3 
                   border border-gray-300 rounded-lg hover:bg-gray-50 
                   transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
			>
				{loading === 'google' ? <span className="animate-spin">⏳</span> : <GoogleIcon />}
				<span>Continuar com Google</span>
			</button>

			<button
				type="button"
				onClick={() => handleOAuth('github')}
				disabled={loading !== null}
				className="w-full flex items-center justify-center gap-3 px-4 py-3 
                   bg-gray-900 text-white rounded-lg hover:bg-gray-800 
                   transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
			>
				{loading === 'github' ? <span className="animate-spin">⏳</span> : <GitHubIcon />}
				<span>Continuar com GitHub</span>
			</button>
		</div>
	);
}

function GoogleIcon() {
	return (
		<svg className="w-5 h-5" viewBox="0 0 24 24">
			<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
			<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
			<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
			<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
		</svg>
	);
}

function GitHubIcon() {
	return (
		<svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
			<path
				fillRule="evenodd"
				d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
				clipRule="evenodd"
			/>
		</svg>
	);
}
```

### Frontend - OAuth Callback Page

```tsx
// frontend/src/app/(auth)/oauth/callback/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

export default function OAuthCallbackPage() {
	const router = useRouter();
	const searchParams = useSearchParams();
	const { setTokens } = useAuth();
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const accessToken = searchParams.get('access_token');
		const refreshToken = searchParams.get('refresh_token');
		const errorParam = searchParams.get('error');

		if (errorParam) {
			setError(getErrorMessage(errorParam));
			return;
		}

		if (accessToken && refreshToken) {
			// Armazenar tokens e redirecionar
			setTokens(accessToken, refreshToken);
			router.push('/chat');
		} else {
			setError('Tokens não recebidos. Tente novamente.');
		}
	}, [searchParams, setTokens, router]);

	if (error) {
		return (
			<div className="min-h-screen flex items-center justify-center">
				<div className="text-center">
					<h1 className="text-2xl font-bold text-red-600 mb-4">Erro na autenticação</h1>
					<p className="text-gray-600 mb-6">{error}</p>
					<a href="/login" className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90">
						Voltar para Login
					</a>
				</div>
			</div>
		);
	}

	return (
		<div className="min-h-screen flex items-center justify-center">
			<div className="text-center">
				<div className="animate-spin text-4xl mb-4">⏳</div>
				<p className="text-gray-600">Autenticando...</p>
			</div>
		</div>
	);
}

function getErrorMessage(error: string): string {
	switch (error) {
		case 'access_denied':
			return 'Acesso negado. Você cancelou a autorização.';
		case 'invalid_state':
			return 'Sessão expirada. Por favor, tente novamente.';
		case 'oauth_failed':
			return 'Falha na autenticação. Por favor, tente novamente.';
		default:
			return `Erro desconhecido: ${error}`;
	}
}
```

### Atualização do useAuth Hook

```typescript
// frontend/src/hooks/useAuth.ts - ADICIONAR

export function useAuth() {
	// ... código existente ...

	const loginWithOAuth = (provider: 'google' | 'github') => {
		window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/oauth/${provider}`;
	};

	const setTokens = (accessToken: string, refreshToken: string) => {
		localStorage.setItem('access_token', accessToken);
		localStorage.setItem('refresh_token', refreshToken);
		// Atualizar estado se necessário
	};

	return {
		// ... existente ...
		loginWithOAuth,
		setTokens,
	};
}
```

### Project Structure Notes

- OAuth usa mesmo modelo `User` já existente - campo `auth_provider` diferencia origem
- Vinculação automática por email permite usuários usarem ambos métodos
- State token previne CSRF - em produção usar Redis ao invés de dict em memória
- Tokens JWT são os mesmos do login tradicional - reutiliza `auth_service.py`
- Frontend callback processa tokens e redireciona - não expõe tokens na URL final

### Padrões da Story 1.2 a Seguir

- Estrutura de pastas: `app/services/`, `app/config/`, `app/api/v1/`
- Nomes de arquivo: snake_case para Python, kebab-case para rotas Next.js
- Configurações: usar Pydantic `BaseSettings` com `@lru_cache`
- Async everywhere: todas as operações de I/O são async
- Tipagem: usar type hints completos, `Mapped[]` para SQLAlchemy

### Segurança - Considerações Importantes

- **State Token**: Gerar com `secrets.token_urlsafe(32)`, validar no callback
- **Tokens em URL**: Evitar em produção - usar httpOnly cookies ou session storage
- **Rate Limiting**: Aplicar nos endpoints OAuth (prevenir brute force)
- **Validação de Email**: Provedores garantem email verificado - não revalidar
- **Secrets**: Client secrets NUNCA no código - sempre env vars

### References

- [Source: architecture.md#Authentication Flow] - Diagrama OAuth
- [Source: architecture.md#API Design] - Endpoints `/oauth/{provider}`
- [Source: architecture.md#Security Measures] - JWT RS256, bcrypt
- [Source: architecture.md#Database Schema] - Campo `auth_provider`
- [Source: epics.md#Story 1.3] - Acceptance criteria originais
- [Source: 1-2-registro-de-usuario-com-email.md] - Padrões estabelecidos

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (via GitHub Copilot)

### Debug Log References

- Todos os 30 testes backend passando (14 existentes + 16 novos OAuth)
- Nenhum erro de lint ou type checking

### Completion Notes List

1. **Task 1-4 (Backend)**: Configuração OAuth completa com Google e GitHub
2. **Task 5-7 (Frontend)**: Botões OAuth, callback handler e hook useAuth atualizados
3. **Task 8 (Testes)**: 16 testes cobrindo URL generation, callbacks, service methods e error handling
4. **Vinculação automática**: Usuários com mesmo email são vinculados automaticamente (AC #3)
5. **Tratamento de erros**: Erros do provedor e cancelamento pelo usuário são tratados gracefully (AC #5)
6. **State CSRF**: Implementado com OAuthStateStore (usar Redis em produção)

### Change Log

| Data       | Arquivo                                         | Mudança                                    |
| ---------- | ----------------------------------------------- | ------------------------------------------ |
| 2026-01-15 | backend/pyproject.toml                          | Adicionado authlib>=1.3.0                  |
| 2026-01-15 | backend/app/config/oauth.py                     | NOVO - Configurações OAuth                 |
| 2026-01-15 | backend/app/schemas/auth.py                     | Adicionado OAuthProvider, OAuthUserInfo    |
| 2026-01-15 | backend/app/services/oauth_service.py           | NOVO - Serviço OAuth completo              |
| 2026-01-15 | backend/app/api/v1/auth.py                      | Adicionados endpoints OAuth                |
| 2026-01-15 | backend/tests/test_oauth.py                     | NOVO - 16 testes OAuth                     |
| 2026-01-15 | frontend/src/components/auth/OAuthButtons.tsx   | NOVO - Botões Google/GitHub                |
| 2026-01-15 | frontend/src/app/(auth)/register/page.tsx       | Integrado OAuthButtons                     |
| 2026-01-15 | frontend/src/app/(auth)/login/page.tsx          | NOVO - Página de login                     |
| 2026-01-15 | frontend/src/app/(auth)/oauth/callback/page.tsx | NOVO - Handler de callback                 |
| 2026-01-15 | frontend/src/hooks/useAuth.ts                   | Adicionado loginWithOAuth, setTokens, etc. |

### File List

**Backend (6 arquivos):**

- backend/pyproject.toml (modificado)
- backend/app/config/oauth.py (novo)
- backend/app/schemas/auth.py (modificado)
- backend/app/services/oauth_service.py (novo)
- backend/app/api/v1/auth.py (modificado)
- backend/tests/test_oauth.py (novo)

**Frontend (5 arquivos):**

- frontend/src/components/auth/OAuthButtons.tsx (novo)
- frontend/src/app/(auth)/register/page.tsx (modificado)
- frontend/src/app/(auth)/login/page.tsx (novo)
- frontend/src/app/(auth)/oauth/callback/page.tsx (novo)
- frontend/src/hooks/useAuth.ts (modificado)
