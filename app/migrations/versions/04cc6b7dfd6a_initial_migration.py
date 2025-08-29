"""initial migration

Revision ID: 04cc6b7dfd6a
Revises:
Create Date: 2025-06-08 21:12:17.279287

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "04cc6b7dfd6a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hotels")
