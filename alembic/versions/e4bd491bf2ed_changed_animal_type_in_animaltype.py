"""Changed Animal_type in AnimalType

Revision ID: e4bd491bf2ed
Revises: 569d21d7bcc4
Create Date: 2024-07-27 13:12:47.110133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4bd491bf2ed'
down_revision: Union[str, None] = '569d21d7bcc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
