"""alter table

Revision ID: d009048aad00
Revises: 12a67ffd63a2
Create Date: 2026-05-15 18:47:40.398454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd009048aad00'
down_revision: Union[str, Sequence[str], None] = '12a67ffd63a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('Users', 'full name', new_column_name='full_name')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('Users', 'full_name', new_column_name='full name')
