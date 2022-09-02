"""Adding User table

Revision ID: c95b05ec4db2
Revises: 
Create Date: 2022-09-02 08:09:10.046378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c95b05ec4db2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('username', sa.String, nullable=False),
                    sa.Column('first_name', sa.String, nullable=False),
                    sa.Column('last_name', sa.String, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('user_type', sa.String, nullable=False),
                    sa.Column('organization', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
