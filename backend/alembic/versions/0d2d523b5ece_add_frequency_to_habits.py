"""add frequency to habits

Revision ID: 0d2d523b5ece
Revises: 581c4cf62edd
Create Date: 2026-10-04 19:58:06.151333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d2d523b5ece'
down_revision: Union[str, Sequence[str], None] = '581c4cf62edd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add frequency column to habits."""
    op.add_column(
        "habits",
        sa.Column(
            "frequency",
            sa.String(length=20),
            nullable=False,
            server_default="daily",
        ),
    )


def downgrade() -> None:
    """Remove frequency column from habits."""
    op.drop_column("habits", "frequency")