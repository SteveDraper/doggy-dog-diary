"""Add dogs table for Phase 1 profiles.

Revision ID: 002
Revises: 001
Create Date: 2026-05-27

"""

from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, Sequence[str], None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE dogs (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            date_of_birth TEXT,
            sex TEXT NOT NULL DEFAULT 'unknown',
            breed TEXT,
            neutered INTEGER,
            microchip TEXT,
            status TEXT NOT NULL DEFAULT 'current',
            status_date TEXT,
            kc_registered_name TEXT,
            kc_number TEXT,
            kc_body TEXT,
            description TEXT,
            profile_photo_path TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    op.execute(
        """
        CREATE INDEX idx_dogs_status_name ON dogs (
            CASE WHEN status = 'current' THEN 0 ELSE 1 END,
            name COLLATE NOCASE
        )
        """
    )
    op.execute(
        """
        UPDATE schema_meta SET value = '1' WHERE key = 'phase'
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_dogs_status_name")
    op.execute("DROP TABLE IF EXISTS dogs")
    op.execute(
        """
        UPDATE schema_meta SET value = '0' WHERE key = 'phase'
        """
    )
