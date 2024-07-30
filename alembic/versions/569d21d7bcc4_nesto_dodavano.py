"""Nesto dodavano

Revision ID: 569d21d7bcc4
Revises: 457a2400ab40
Create Date: 2024-07-27 12:42:23.317701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '569d21d7bcc4'
down_revision: Union[str, None] = '457a2400ab40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
