"""empty message

Revision ID: b3a28c3fe2ec
Revises: 
Create Date: 2022-06-10 23:40:59.302480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a28c3fe2ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('top',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=62), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('mid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=62), nullable=True),
    sa.Column('Schema', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Schema'], ['top.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bottom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=62), nullable=True),
    sa.Column('mid_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mid_id'], ['mid.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bottom')
    op.drop_table('mid')
    op.drop_table('top')
    # ### end Alembic commands ###
