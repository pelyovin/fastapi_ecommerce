"""fix rating and review models

Revision ID: e445d87d6c72
Revises: 2aa0b1e8aa1d
Create Date: 2024-12-07 17:53:50.646640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e445d87d6c72'
down_revision: Union[str, None] = '2aa0b1e8aa1d'
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