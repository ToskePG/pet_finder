"""Changed animal to pet

Revision ID: 26e8527b2fe2
Revises: bd3ef07913c6
Create Date: 2024-07-30 18:44:05.504354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26e8527b2fe2'
down_revision: Union[str, None] = 'bd3ef07913c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
