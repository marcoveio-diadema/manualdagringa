"""blogpost model modified

Revision ID: 414cdce49728
Revises: 7acb700f87cd
Create Date: 2024-01-03 14:59:00.528623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414cdce49728'
down_revision = '7acb700f87cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body_2', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('middle_link', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('img_background', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('img_1', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('img_2', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('img_3', sa.String(length=500), nullable=True))
        batch_op.drop_column('img_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img_url', sa.VARCHAR(length=500), nullable=False))
        batch_op.drop_column('img_3')
        batch_op.drop_column('img_2')
        batch_op.drop_column('img_1')
        batch_op.drop_column('img_background')
        batch_op.drop_column('middle_link')
        batch_op.drop_column('body_2')

    # ### end Alembic commands ###
