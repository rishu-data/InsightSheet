"""grandfather_existing_users_as_verified

Revision ID: e96369d9fd88
Revises: 34a3d853481e
"""
from typing import Sequence, Union

from alembic import op

revision: str = 'e96369d9fd88'
down_revision: Union[str, Sequence[str], None] = '34a3d853481e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('UPDATE app_user\nSET email_verified_at = COALESCE(created_at, NOW())\nWHERE email_verified_at IS NULL;')


def downgrade() -> None:
    pass
