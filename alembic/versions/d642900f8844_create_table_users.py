"""create_table_users

Revision ID: d642900f8844
Revises: 9d91f805abff
Create Date: 2023-07-30 14:21:07.811378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd642900f8844'
down_revision = '9d91f805abff'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("NOW()")),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )



def downgrade() -> None:
    op.drop_table('users')
