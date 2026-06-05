"""add in moderation form status

Revision ID: add_in_moderation_form_status
Revises: 0acd6c73f3dd
Create Date: 2026-05-29 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "add_in_moderation_form_status"
down_revision: Union[str, Sequence[str], None] = "0acd6c73f3dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE formstatus ADD VALUE IF NOT EXISTS 'IN_MODERATION'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
