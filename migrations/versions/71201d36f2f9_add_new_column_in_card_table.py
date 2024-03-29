"""add new column in card table

Revision ID: 71201d36f2f9
Revises: 5cb43264a827
Create Date: 2023-07-13 21:37:52.968607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71201d36f2f9'
down_revision = '5cb43264a827'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Card_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('successfully_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('last_repetition', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('inter_repetition_interval', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Card_table', schema=None) as batch_op:
        batch_op.drop_column('inter_repetition_interval')
        batch_op.drop_column('last_repetition')
        batch_op.drop_column('successfully_count')

    # ### end Alembic commands ###
