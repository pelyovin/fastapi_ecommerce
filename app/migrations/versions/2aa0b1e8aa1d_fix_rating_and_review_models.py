"""fix rating and review models

Revision ID: 2aa0b1e8aa1d
Revises: 2a98602b4e93
Create Date: 2024-12-07 17:49:16.701574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aa0b1e8aa1d'
down_revision: Union[str, None] = '2a98602b4e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
