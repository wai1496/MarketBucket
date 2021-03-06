"""added a products table

Revision ID: 2c6627601de0
Revises: 7a13fe95fd47
Create Date: 2019-01-09 13:35:58.230002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c6627601de0'
down_revision = '7a13fe95fd47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('marketplace_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=64), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['marketplace_id'], ['marketplaces.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_name')
    )
    op.add_column('images', sa.Column('product_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'images', 'products', ['product_id'], ['id'])
    op.create_unique_constraint(None, 'users', ['store_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.drop_column('images', 'product_id')
    op.drop_table('products')
    # ### end Alembic commands ###
