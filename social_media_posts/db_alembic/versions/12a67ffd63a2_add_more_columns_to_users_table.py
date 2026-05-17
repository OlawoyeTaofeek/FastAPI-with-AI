"""Add more columns to users Table

Revision ID: 12a67ffd63a2
Revises: 54d5ca599d75
Create Date: 2026-05-15 17:53:15.413421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12a67ffd63a2'
down_revision: Union[str, Sequence[str], None] = '54d5ca599d75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Users', sa.Column('full name', sa.String(255), nullable=False))
    op.add_column('Users', sa.Column("bio", sa.String(500), nullable=True))
    op.add_column("Users", sa.Column("username", sa.String(100), nullable=False, unique=True))
    # op.add_column("Users", sa.Column("profile_picture_url", sa.String(255), nullable=True))
    # op.add_column("Users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()))
    op.add_column("Users", sa.Column("country", sa.String(100), nullable=True))
    op.add_column("Users", sa.Column("date_of_birth", sa.Date(), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Users', 'full name')
    op.drop_column('Users', 'bio')
    op.drop_column('Users', 'username')
    # op.drop_column('Users', 'profile_picture_url')
    # op.drop_column('Users', 'is_active')
    op.drop_column('Users', 'country')
    op.drop_column('Users', 'date_of_birth')
