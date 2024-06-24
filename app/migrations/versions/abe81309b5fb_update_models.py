"""Update models

Revision ID: abe81309b5fb
Revises: f1e0fdd90261
Create Date: 2024-06-08 22:59:41.858686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'abe81309b5fb'
down_revision: Union[str, None] = 'f1e0fdd90261'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookings', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('hotels', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('hotels', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('hotels', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('hotels', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bookings', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###