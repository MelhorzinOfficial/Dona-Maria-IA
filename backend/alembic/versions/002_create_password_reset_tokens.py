"""
Create password reset tokens table

Revision ID: 002_create_password_reset_tokens
Revises: 001_create_users_table
Create Date: 2026-01-15
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "002_create_password_reset_tokens"
down_revision: str = "001_create_users_table"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create password reset tokens table."""
    op.create_table(
        "password_reset_tokens",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index("idx_password_reset_token_hash", "password_reset_tokens", ["token_hash"])
    op.create_index("idx_password_reset_user_id", "password_reset_tokens", ["user_id"])
    op.create_index("idx_password_reset_expires", "password_reset_tokens", ["expires_at"])


def downgrade() -> None:
    """Drop password reset tokens table."""
    op.drop_index("idx_password_reset_expires", table_name="password_reset_tokens")
    op.drop_index("idx_password_reset_user_id", table_name="password_reset_tokens")
    op.drop_index("idx_password_reset_token_hash", table_name="password_reset_tokens")
    op.drop_table("password_reset_tokens")