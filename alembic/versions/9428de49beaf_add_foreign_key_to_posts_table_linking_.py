"""Add foreign key to posts table linking to users table

Revision ID: 9428de49beaf
Revises: c72210f9e129
Create Date: 2026-04-07 20:52:44.570059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9428de49beaf'
down_revision: Union[str, Sequence[str], None] = 'c72210f9e129'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
        'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    pass
