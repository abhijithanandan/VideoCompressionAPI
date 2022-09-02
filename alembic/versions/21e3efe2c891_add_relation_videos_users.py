"""Add relation videos users

Revision ID: 21e3efe2c891
Revises: d1593ccf12c4
Create Date: 2022-09-02 09:59:19.866712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21e3efe2c891'
down_revision = 'd1593ccf12c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('videos', sa.Column('user_id', sa.Integer, nullable=False))
    op.create_foreign_key('video_user_fk', source_table='videos', referent_table='users', local_cols=['user_id'],
                          remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('video_user_fk')
    op.drop_column('videos', 'user_id')
