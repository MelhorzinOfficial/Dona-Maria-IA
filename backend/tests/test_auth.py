"""
Tests for authentication endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.auth_service import verify_password


class TestRegister:
    """Tests for the registration endpoint."""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient) -> None:
        """Test successful user registration returns tokens."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_register_creates_user_in_database(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Test that registration creates user in the database."""
        email = "newuser@example.com"
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "password123",
            },
        )
        assert response.status_code == 201

        # Verify user exists in database
        stmt = select(User).where(User.email == email.lower())
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        assert user is not None
        assert user.email == email.lower()
        assert user.auth_provider == "email"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient) -> None:
        """Test that registering with duplicate email fails."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "password123",
        }

        # First registration
        response1 = await client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201

        # Second registration with same email
        response2 = await client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "já cadastrado" in response2.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_short_password(self, client: AsyncClient) -> None:
        """Test that registration fails with password < 8 characters."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "short@example.com",
                "password": "123",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient) -> None:
        """Test that registration fails with invalid email format."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_empty_email(self, client: AsyncClient) -> None:
        """Test that registration fails with empty email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_empty_password(self, client: AsyncClient) -> None:
        """Test that registration fails with empty password."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "empty@example.com",
                "password": "",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_password_is_hashed_with_bcrypt(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Test that password is hashed with bcrypt cost factor 12."""
        email = "bcrypt@example.com"
        password = "password123"

        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == 201

        # Get user from database
        stmt = select(User).where(User.email == email.lower())
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        assert user is not None
        assert user.password_hash is not None
        # Bcrypt hash with cost factor 12 starts with $2b$12$
        assert user.password_hash.startswith("$2b$12$")
        # Verify password can be verified
        assert verify_password(password, user.password_hash)

    @pytest.mark.asyncio
    async def test_register_email_case_insensitive(
        self, client: AsyncClient
    ) -> None:
        """Test that email registration is case-insensitive."""
        # Register with uppercase
        response1 = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "TEST@EXAMPLE.COM",
                "password": "password123",
            },
        )
        assert response1.status_code == 201

        # Try to register with lowercase same email
        response2 = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password456",
            },
        )
        assert response2.status_code == 400
        assert "já cadastrado" in response2.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_password_exactly_8_chars(
        self, client: AsyncClient
    ) -> None:
        """Test that password with exactly 8 characters is accepted."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "exact8@example.com",
                "password": "12345678",
            },
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_register_password_7_chars_rejected(
        self, client: AsyncClient
    ) -> None:
        """Test that password with 7 characters is rejected."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "seven@example.com",
                "password": "1234567",
            },
        )
        assert response.status_code == 422


class TestLogin:
    """Tests for the login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient) -> None:
        """Test successful login returns tokens."""
        # First register a user
        email = "login@example.com"
        password = "password123"
        await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password},
        )

        # Then login
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient) -> None:
        """Test login with wrong password returns 401."""
        email = "wrongpass@example.com"
        await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "password123"},
        )

        response = await client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert "Email ou senha incorretos" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient) -> None:
        """Test login with nonexistent email returns 401."""
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent@example.com", "password": "password123"},
        )
        assert response.status_code == 401
        assert "Email ou senha incorretos" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_email_case_insensitive(self, client: AsyncClient) -> None:
        """Test login works with different email case."""
        await client.post(
            "/api/v1/auth/register",
            json={"email": "case@example.com", "password": "password123"},
        )

        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "CASE@EXAMPLE.COM", "password": "password123"},
        )
        assert response.status_code == 200


class TestLogout:
    """Tests for the logout endpoint."""

    @pytest.mark.asyncio
    async def test_logout_success(self, client: AsyncClient) -> None:
        """Test logout with valid token returns success message."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "logout@example.com", "password": "password123"},
        )
        login_response = await client.post(
            "/api/v1/auth/login",
            data={"username": "logout@example.com", "password": "password123"},
        )
        access_token = login_response.json()["access_token"]

        # Logout
        response = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert "Logout realizado com sucesso" in response.json()["message"]

    @pytest.mark.asyncio
    async def test_logout_without_token(self, client: AsyncClient) -> None:
        """Test logout without token returns 401."""
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 401


class TestRefreshToken:
    """Tests for the refresh token endpoint."""

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client: AsyncClient) -> None:
        """Test refresh token generates new access token."""
        # Register and get tokens
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "refresh@example.com", "password": "password123"},
        )
        refresh_token = response.json()["refresh_token"]

        # Refresh
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, client: AsyncClient) -> None:
        """Test invalid refresh token returns 401."""
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"},
        )
        assert response.status_code == 401
        assert "Sessão expirada" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_refresh_token_using_access_token(self, client: AsyncClient) -> None:
        """Test using access token as refresh token fails."""
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "wrongtype@example.com", "password": "password123"},
        )
        access_token = response.json()["access_token"]

        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token},
        )
        assert response.status_code == 401
