"""Update rooms model

Revision ID: f1e0fdd90261
Revises: b56b4262b583
Create Date: 2024-06-05 23:15:43.471009

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1e0fdd90261"
down_revision: Union[str, None] = "b56b4262b583"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("rooms", "description", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("rooms", "description", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
