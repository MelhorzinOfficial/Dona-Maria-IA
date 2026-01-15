"""
Authentication API Router.

Endpoints para registro e autenticação de usuários.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.config.database import get_db
from app.config.oauth import oauth_settings
from app.schemas.auth import OAuthProvider, RefreshTokenRequest, Token, UserCreate
from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ForgotPasswordResponse
)
from app.services.password_reset_service import PasswordResetService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Registrar novo usuário com email e senha.

    Args:
        user_data: Dados de registro (email e senha).
        db: Sessão do banco de dados.

    Returns:
        Token: Tokens JWT de acesso e refresh.

    Raises:
        HTTPException: Se email já estiver cadastrado.
    """
    auth_service = AuthService(db)

    # Verificar se email já existe
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )

    # Criar usuário
    user = await auth_service.create_user(user_data)

    # Gerar tokens
    tokens = auth_service.create_tokens(user.id)

    return Token(**tokens)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Fazer login com email e senha.

    Args:
        form_data: Email (username) e senha do usuário.
        db: Sessão do banco de dados.

    Returns:
        Token: Tokens JWT de acesso e refresh.

    Raises:
        HTTPException: Se credenciais inválidas.
    """
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


@router.post("/logout")
async def logout(
    current_user: CurrentUser,
) -> dict:
    """
    Fazer logout do usuário atual.

    Remove tokens do lado do cliente. Sessão Redis será implementada
    quando rate limiting for adicionado.

    Args:
        current_user: Usuário autenticado.

    Returns:
        Mensagem de sucesso.
    """
    # No MVP, logout é feito removendo tokens no cliente.
    # Sessão Redis é preparada mas não obrigatória para AC.
    return {"message": "Logout realizado com sucesso"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Renovar access token usando refresh token.

    Args:
        request: Refresh token para validação.
        db: Sessão do banco de dados.

    Returns:
        Novos tokens JWT.

    Raises:
        HTTPException: Se refresh token inválido ou expirado.
    """
    # Verificar refresh token
    token_data = verify_token(request.refresh_token, token_type="refresh")
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se usuário existe
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gerar novos tokens
    tokens = auth_service.create_tokens(user.id)
    return Token(**tokens)


@router.get("/oauth/{provider}")
async def oauth_redirect(provider: OAuthProvider) -> RedirectResponse:
    """
    Iniciar fluxo OAuth redirecionando para o provedor.

    Args:
        provider: Provedor OAuth (google ou github).

    Returns:
        RedirectResponse para URL de autorização do provedor.
    """
    oauth_service = OAuthService(db=None)  # type: ignore - não precisa de DB para gerar URL
    authorize_url, state = oauth_service.generate_oauth_url(provider.value)

    # Criar resposta de redirecionamento
    response = RedirectResponse(url=authorize_url, status_code=302)

    # Armazenar state em cookie httpOnly para validação no callback
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        secure=False,  # True em produção com HTTPS
        max_age=600,  # 10 minutos
        samesite="lax",
    )

    return response


@router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: OAuthProvider,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    error_description: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """
    Callback do provedor OAuth.

    Troca code por token e cria/vincula usuário.

    Args:
        provider: Provedor OAuth.
        code: Authorization code do provedor.
        state: State token para validação CSRF.
        error: Código de erro do provedor (se houver).
        error_description: Descrição do erro.
        db: Sessão do banco de dados.

    Returns:
        RedirectResponse para frontend com tokens ou erro.
    """
    frontend_url = oauth_settings.frontend_url

    # Verificar erro do provedor (usuário cancelou ou provedor indisponível)
    if error:
        error_msg = error_description or error
        return RedirectResponse(
            url=f"{frontend_url}/login?error={error_msg}",
            status_code=302,
        )

    # Validar presença de code e state
    if not code or not state:
        return RedirectResponse(
            url=f"{frontend_url}/login?error=missing_params",
            status_code=302,
        )

    oauth_service = OAuthService(db)

    # Validar state token (previne CSRF)
    if not oauth_service.validate_state(state):
        return RedirectResponse(
            url=f"{frontend_url}/login?error=invalid_state",
            status_code=302,
        )

    try:
        # Trocar code por access token do provedor
        access_token = await oauth_service.exchange_code_for_token(
            provider.value, code
        )

        # Buscar informações do usuário do provedor
        user_info = await oauth_service.get_user_info(provider.value, access_token)

        # Criar ou vincular usuário no banco
        user = await oauth_service.get_or_create_user(user_info)

        # Gerar JWT tokens para nossa aplicação
        auth_service = AuthService(db)
        tokens = auth_service.create_tokens(user.id)

        # Redirecionar para frontend com tokens
        callback_url = (
            f"{frontend_url}/oauth/callback"
            f"?access_token={tokens['access_token']}"
            f"&refresh_token={tokens['refresh_token']}"
        )
        return RedirectResponse(url=callback_url, status_code=302)

    except ValueError as e:
        # Erro de validação (email não disponível, etc)
        return RedirectResponse(
            url=f"{frontend_url}/login?error={str(e)}",
            status_code=302,
        )
    except Exception:
        # Erro genérico (provedor indisponível, etc)
        return RedirectResponse(
            url=f"{frontend_url}/login?error=oauth_failed",
            status_code=302,
        )


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Solicitar link de reset de senha via email.

    Sempre retorna sucesso para não revelar se email existe.
    """
    service = PasswordResetService(db)
    await service.request_reset(request.email)

    return ForgotPasswordResponse(
        message="Se o email estiver cadastrado, você receberá um link de recuperação."
    )


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Resetar senha usando token válido.
    """
    service = PasswordResetService(db)
    success = await service.reset_password(request.token, request.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Link expirado ou inválido. Solicite um novo link."
        )

    return {"message": "Senha alterada com sucesso. Faça login com sua nova senha."}


@router.get("/verify-reset-token/{token}")
async def verify_reset_token(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Verificar se token de reset é válido (para UI mostrar form ou erro).
    """
    service = PasswordResetService(db)
    reset_token = await service.verify_token(token)

    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Link expirado ou inválido."
        )

    return {"valid": True}

