"""creat users table

Revision ID: 3792f6e350f8
Revises: 4d9b397d8fd0
Create Date: 2022-11-24 19:30:32.673653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3792f6e350f8'
down_revision = '4d9b397d8fd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('username',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
)
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
