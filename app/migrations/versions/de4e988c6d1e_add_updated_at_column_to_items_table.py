"""Add updated_at column to items table

Revision ID: de4e988c6d1e
Revises: 
Create Date: 2025-10-29 13:11:55.227250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de4e988c6d1e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add updated_at column to items table
    op.add_column('items',
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove updated_at column from items table
    op.drop_column('items', 'updated_at')
