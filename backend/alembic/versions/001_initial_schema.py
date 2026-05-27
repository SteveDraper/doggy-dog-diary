"""Initial schema placeholder for Phase 0 skeleton.

Revision ID: 001
Revises:
Create Date: 2026-05-26

"""

from typing import Sequence, Union

from alembic import op

revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Phase 0: migrations run; domain tables arrive in Phase 1."""
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    op.execute(
        """
        INSERT OR IGNORE INTO schema_meta (key, value)
        VALUES ('phase', '0')
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS schema_meta")
