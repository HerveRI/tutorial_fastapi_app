"""add content column to posts table

Revision ID: a21731dc3ad4
Revises: 4917fb04e022
Create Date: 2026-04-07 20:26:24.704219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a21731dc3ad4'
down_revision: Union[str, Sequence[str], None] = '4917fb04e022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
