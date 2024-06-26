"""Auto increment move id

Revision ID: c82da1e02fc4
Revises: 25ee977b3a2d
Create Date: 2024-06-05 15:32:05.112516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c82da1e02fc4'
down_revision = '25ee977b3a2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_movement', schema=None) as batch_op:
        batch_op.alter_column('movement_id',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_movement', schema=None) as batch_op:
        batch_op.alter_column('movement_id',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
