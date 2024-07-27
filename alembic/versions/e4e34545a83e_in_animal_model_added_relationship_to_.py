"""In Animal model added relationship to animal_type

Revision ID: e4e34545a83e
Revises: e4bd491bf2ed
Create Date: 2024-07-27 14:48:41.907756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4e34545a83e'
down_revision: Union[str, None] = 'e4bd491bf2ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
