"""added test_type and is_practice_test to test DB

Revision ID: 5d9176b68d79
Revises: 3849b2658e6a
Create Date: 2025-05-09 18:05:58.847011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d9176b68d79'
down_revision: Union[str, None] = '3849b2658e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tests_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test_type', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('is_practice_test', sa.BOOLEAN(), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tests_table', schema=None) as batch_op:
        batch_op.drop_column('is_practice_test')
        batch_op.drop_column('test_type')

    # ### end Alembic commands ###
