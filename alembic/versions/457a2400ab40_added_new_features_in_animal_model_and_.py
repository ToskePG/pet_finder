"""Added new features in Animal model and User model

Revision ID: 457a2400ab40
Revises: 8bc2b441f879
Create Date: 2024-07-27 10:33:58.173751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '457a2400ab40'
down_revision: Union[str, None] = '8bc2b441f879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
