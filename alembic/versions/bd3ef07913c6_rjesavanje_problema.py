"""Rjesavanje problema

Revision ID: bd3ef07913c6
Revises: e4e34545a83e
Create Date: 2024-07-27 15:22:33.333602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd3ef07913c6'
down_revision: Union[str, None] = 'e4e34545a83e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
