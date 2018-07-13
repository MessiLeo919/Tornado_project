"""add creat for post

Revision ID: d9aa037c6839
Revises: 0c35b7ddf227
Create Date: 2018-07-13 14:06:55.610981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9aa037c6839'
down_revision = '0c35b7ddf227'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'created')
    # ### end Alembic commands ###
