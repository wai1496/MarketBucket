"""removed fk from images

Revision ID: 35232e2a9dc2
Revises: 2c6627601de0
Create Date: 2019-01-19 17:49:16.832527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35232e2a9dc2'
down_revision = '2c6627601de0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('images_product_id_fkey', 'images', type_='foreignkey')
    op.drop_column('images', 'product_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('images_product_id_fkey', 'images', 'products', ['product_id'], ['id'])
    # ### end Alembic commands ###
