"""upgrade

Revision ID: 8bc2b441f879
Revises: 6eb5ea5b058d
Create Date: 2024-07-26 15:50:44.038598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc2b441f879'
down_revision: Union[str, None] = '6eb5ea5b058d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
