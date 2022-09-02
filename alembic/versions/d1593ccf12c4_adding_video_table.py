"""Adding Video table

Revision ID: d1593ccf12c4
Revises: c95b05ec4db2
Create Date: 2022-09-02 09:43:19.304652

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd1593ccf12c4'
down_revision = 'c95b05ec4db2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('videos',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('description', sa.String, default=f"Video uploaded for compression", nullable=False),
                    sa.Column('uri', sa.String, nullable=False),
                    sa.Column('upload_time', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()'))
                    )


def downgrade() -> None:
    op.drop_table('videos')
