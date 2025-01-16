"""add content column to posts table

Revision ID: 3edf7d37f99c
Revises: 0f1945b3c54c
Create Date: 2025-01-16 18:10:06.617949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3edf7d37f99c'
down_revision: Union[str, None] = '0f1945b3c54c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
