"""
Tests for OAuth authentication endpoints.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import OAuthProvider, OAuthUserInfo
from app.services.oauth_service import OAuthService, state_store


class TestOAuthURLGeneration:
    """Tests for OAuth URL generation."""

    @pytest.mark.asyncio
    async def test_generate_google_oauth_url(self, client: AsyncClient) -> None:
        """Test that Google OAuth URL is generated correctly."""
        response = await client.get(
            "/api/v1/auth/oauth/google",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "accounts.google.com" in location
        assert "client_id=" in location
        assert "redirect_uri=" in location
        assert "state=" in location
        assert "scope=" in location

    @pytest.mark.asyncio
    async def test_generate_github_oauth_url(self, client: AsyncClient) -> None:
        """Test that GitHub OAuth URL is generated correctly."""
        response = await client.get(
            "/api/v1/auth/oauth/github",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "github.com/login/oauth" in location
        assert "client_id=" in location
        assert "redirect_uri=" in location
        assert "state=" in location

    @pytest.mark.asyncio
    async def test_oauth_sets_state_cookie(self, client: AsyncClient) -> None:
        """Test that OAuth redirect sets state cookie."""
        response = await client.get(
            "/api/v1/auth/oauth/google",
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "oauth_state" in response.cookies

    @pytest.mark.asyncio
    async def test_invalid_provider_returns_422(self, client: AsyncClient) -> None:
        """Test that invalid OAuth provider returns 422."""
        response = await client.get(
            "/api/v1/auth/oauth/invalid_provider",
            follow_redirects=False,
        )
        assert response.status_code == 422


class TestOAuthCallback:
    """Tests for OAuth callback endpoint."""

    @pytest.mark.asyncio
    async def test_callback_without_code_redirects_with_error(
        self, client: AsyncClient
    ) -> None:
        """Test callback without code redirects to login with error."""
        response = await client.get(
            "/api/v1/auth/oauth/google/callback",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "/login" in location
        assert "error=" in location

    @pytest.mark.asyncio
    async def test_callback_with_error_param_redirects(
        self, client: AsyncClient
    ) -> None:
        """Test callback with error param redirects to login."""
        response = await client.get(
            "/api/v1/auth/oauth/google/callback?error=access_denied",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "/login" in location
        assert "access_denied" in location

    @pytest.mark.asyncio
    async def test_callback_with_invalid_state_redirects_error(
        self, client: AsyncClient
    ) -> None:
        """Test callback with invalid state redirects with error."""
        response = await client.get(
            "/api/v1/auth/oauth/google/callback?code=test_code&state=invalid_state",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "invalid_state" in location

    @pytest.mark.asyncio
    async def test_callback_success_creates_user(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Test successful OAuth callback creates new user."""
        # Create a valid state
        valid_state = state_store.create_state()

        # Mock the OAuth service methods
        with patch.object(
            OAuthService, "exchange_code_for_token", new_callable=AsyncMock
        ) as mock_exchange, patch.object(
            OAuthService, "get_user_info", new_callable=AsyncMock
        ) as mock_info:
            mock_exchange.return_value = "mock_access_token"
            mock_info.return_value = OAuthUserInfo(
                provider=OAuthProvider.GOOGLE,
                provider_user_id="12345",
                email="oauth_user@example.com",
                name="OAuth User",
                avatar_url="https://example.com/avatar.jpg",
            )

            response = await client.get(
                f"/api/v1/auth/oauth/google/callback?code=valid_code&state={valid_state}",
                follow_redirects=False,
            )

            assert response.status_code == 302
            location = response.headers.get("location", "")
            assert "/oauth/callback" in location
            assert "access_token=" in location
            assert "refresh_token=" in location

    @pytest.mark.asyncio
    async def test_callback_links_existing_user(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Test OAuth callback links to existing user with same email."""
        # Create existing user
        existing_user = User(
            email="existing@example.com",
            password_hash="$2b$12$test_hash",
            auth_provider="email",
        )
        db_session.add(existing_user)
        await db_session.commit()

        # Create valid state
        valid_state = state_store.create_state()

        with patch.object(
            OAuthService, "exchange_code_for_token", new_callable=AsyncMock
        ) as mock_exchange, patch.object(
            OAuthService, "get_user_info", new_callable=AsyncMock
        ) as mock_info:
            mock_exchange.return_value = "mock_access_token"
            mock_info.return_value = OAuthUserInfo(
                provider=OAuthProvider.GITHUB,
                provider_user_id="67890",
                email="existing@example.com",
                name="Existing User",
                avatar_url="https://github.com/avatar.jpg",
            )

            response = await client.get(
                f"/api/v1/auth/oauth/github/callback?code=valid_code&state={valid_state}",
                follow_redirects=False,
            )

            assert response.status_code == 302

            # Verify user wasn't duplicated
            stmt = select(User).where(User.email == "existing@example.com")
            result = await db_session.execute(stmt)
            users = result.scalars().all()
            assert len(users) == 1

            # Verify auth_provider wasn't changed (keeps original)
            assert users[0].auth_provider == "email"


class TestOAuthService:
    """Tests for OAuth service methods."""

    def test_state_store_create_and_validate(self) -> None:
        """Test state store creates and validates states."""
        state = state_store.create_state()
        assert len(state) > 20  # Secure random string
        assert state_store.validate_state(state) is True
        # State should be consumed after validation
        assert state_store.validate_state(state) is False

    def test_state_store_invalid_state(self) -> None:
        """Test state store rejects invalid states."""
        assert state_store.validate_state("invalid_state") is False

    @pytest.mark.asyncio
    async def test_get_or_create_user_creates_new(
        self, db_session: AsyncSession
    ) -> None:
        """Test get_or_create_user creates new user."""
        service = OAuthService(db_session)
        user_info = OAuthUserInfo(
            provider=OAuthProvider.GOOGLE,
            provider_user_id="new_user_123",
            email="new_oauth@example.com",
            name="New OAuth User",
            avatar_url="https://example.com/new_avatar.jpg",
        )

        user = await service.get_or_create_user(user_info)

        assert user.email == "new_oauth@example.com"
        assert user.auth_provider == "google"
        assert user.display_name == "New OAuth User"
        assert user.avatar_url == "https://example.com/new_avatar.jpg"
        assert user.password_hash is None

    @pytest.mark.asyncio
    async def test_get_or_create_user_links_existing(
        self, db_session: AsyncSession
    ) -> None:
        """Test get_or_create_user links to existing user."""
        # Create existing user without avatar
        existing = User(
            email="link_test@example.com",
            password_hash="$2b$12$hash",
            auth_provider="email",
        )
        db_session.add(existing)
        await db_session.commit()
        existing_id = existing.id

        service = OAuthService(db_session)
        user_info = OAuthUserInfo(
            provider=OAuthProvider.GITHUB,
            provider_user_id="github_123",
            email="link_test@example.com",
            name="GitHub Name",
            avatar_url="https://github.com/avatar.jpg",
        )

        user = await service.get_or_create_user(user_info)

        # Should return same user
        assert user.id == existing_id
        # Should update avatar (was None)
        assert user.avatar_url == "https://github.com/avatar.jpg"
        # Should NOT change auth_provider
        assert user.auth_provider == "email"


class TestOAuthErrorHandling:
    """Tests for OAuth error handling."""

    @pytest.mark.asyncio
    async def test_provider_error_redirects_gracefully(
        self, client: AsyncClient
    ) -> None:
        """Test that provider errors redirect gracefully."""
        response = await client.get(
            "/api/v1/auth/oauth/google/callback?error=server_error&error_description=Provider+unavailable",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "/login" in location

    @pytest.mark.asyncio
    async def test_user_cancel_handled(self, client: AsyncClient) -> None:
        """Test that user cancellation is handled gracefully."""
        response = await client.get(
            "/api/v1/auth/oauth/github/callback?error=access_denied&error_description=The+user+denied+access",
            follow_redirects=False,
        )
        assert response.status_code == 302
        location = response.headers.get("location", "")
        assert "access_denied" in location or "error" in location

    @pytest.mark.asyncio
    async def test_oauth_failure_redirects_with_error(
        self, client: AsyncClient
    ) -> None:
        """Test that OAuth failures redirect with generic error."""
        valid_state = state_store.create_state()

        with patch.object(
            OAuthService, "exchange_code_for_token", new_callable=AsyncMock
        ) as mock_exchange:
            mock_exchange.side_effect = Exception("Network error")

            response = await client.get(
                f"/api/v1/auth/oauth/google/callback?code=valid&state={valid_state}",
                follow_redirects=False,
            )

            assert response.status_code == 302
            location = response.headers.get("location", "")
            assert "oauth_failed" in location or "error" in location
