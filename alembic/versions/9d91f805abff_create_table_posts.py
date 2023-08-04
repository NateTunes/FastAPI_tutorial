"""create_table_posts

Revision ID: 9d91f805abff
Revises:
Create Date: 2023-07-30 13:47:36.832395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d91f805abff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('content', sa.String, nullable=False),
                    sa.Column('published', sa.String, server_default="TRUE", nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()"))
                    )


def downgrade() -> None:
    op.drop_table('posts')
