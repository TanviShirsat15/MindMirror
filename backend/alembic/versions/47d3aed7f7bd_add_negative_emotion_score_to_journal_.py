"""add negative emotion score to journal analysis

Revision ID: 47d3aed7f7bd
Revises: 0d2d523b5ece
Create Date: 2026-10-05 01:43:10.602554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "47d3aed7f7bd"
down_revision: Union[str, Sequence[str], None] = "0d2d523b5ece"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add negative emotion score to journal analysis."""
    op.add_column(
        "journal_analysis",
        sa.Column(
            "negative_emotion_score",
            sa.Float(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove negative emotion score from journal analysis."""
    op.drop_column("journal_analysis", "negative_emotion_score")