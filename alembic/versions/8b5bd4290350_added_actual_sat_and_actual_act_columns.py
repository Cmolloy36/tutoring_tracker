"""added actual_SAT and actual_ACT columns

Revision ID: 8b5bd4290350
Revises: 
Create Date: 2025-05-06 09:52:58.241433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b5bd4290350'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('students_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('actual_SAT',sa.Integer(),nullable=True,default=None))
        batch_op.add_column(sa.Column('actual_ACT',sa.Integer(),nullable=True,default=None))


def downgrade() -> None:
    with op.batch_alter_table('students_table', schema=None) as batch_op:
        batch_op.drop_column('actual_SAT')
        batch_op.drop_column('actual_ACT')
