"""role permissions added as bool columns

Revision ID: 4591b13885c3
Revises: 
Create Date: 2025-08-02 00:53:05.732923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4591b13885c3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'user_roles',
        sa.Column('can_create_user', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_user', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_user', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_user', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_create_role', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_role', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_role', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_role', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_create_patient', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_patient', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_patient', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_patient', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_create_entry', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_entry', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_entry', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_entry', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_create_prediction', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_prediction', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_prediction', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_prediction', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_create_feedback', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_feedback', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_feedback', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_feedback', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_create_report', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_edit_report', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_delete_report', sa.Boolean(), nullable=False, server_default='false')
    )

    op.add_column(
        'user_roles',
        sa.Column('can_view_report', sa.Boolean(), nullable=False, server_default='false')
    )

def downgrade() -> None:
    pass
