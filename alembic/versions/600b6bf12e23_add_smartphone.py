"""add smartphone

Revision ID: 600b6bf12e23
Revises: 
Create Date: 2023-01-28 14:42:55.814603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '600b6bf12e23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopkz_smartphone',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('memory', sa.String(length=20), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shopkz_smartphone_price'), 'shopkz_smartphone', ['price'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shopkz_smartphone_price'), table_name='shopkz_smartphone')
    op.drop_table('shopkz_smartphone')
    # ### end Alembic commands ###
