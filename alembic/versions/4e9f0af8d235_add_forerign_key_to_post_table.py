"""add forerign-key to post table

Revision ID: 4e9f0af8d235
Revises: d642900f8844
Create Date: 2023-07-30 14:26:02.705669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e9f0af8d235'
down_revision = 'd642900f8844'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', 'posts')
    op.drop_column('posts', 'owner_id')
