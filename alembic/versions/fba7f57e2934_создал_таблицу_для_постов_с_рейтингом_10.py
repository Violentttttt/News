"""Создал таблицу для постов с рейтингом 10

Revision ID: fba7f57e2934
Revises: a721f5d9330a
Create Date: 2024-09-03 23:39:42.474685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fba7f57e2934'
down_revision: Union[str, None] = 'a721f5d9330a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rate10',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=False),
    sa.Column('rate', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=500), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rate10'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rate10')
    # ### end Alembic commands ###
