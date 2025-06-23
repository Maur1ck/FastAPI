"""add users

Revision ID: 731b98c6cc57
Revises: c6574e563440
Create Date: 2025-06-23 11:16:53.932656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "731b98c6cc57"
down_revision: Union[str, None] = "c6574e563440"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
