"""Added models

Revision ID: 3f29eb2d81c8
Revises: 
Create Date: 2024-07-09 20:32:23.814383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f29eb2d81c8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('company_name', sa.String(length=30), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('sales_contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sales_contact_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contract_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_balance', sa.Float(), nullable=False),
    sa.Column('remaining_balance', sa.Float(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'SIGNED', 'FINISHED', name='contractstatus'), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_start_date', sa.DateTime(), nullable=False),
    sa.Column('event_end_date', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=30), nullable=False),
    sa.Column('attendees', sa.Integer(), nullable=False),
    sa.Column('notes', sa.String(length=30), nullable=False),
    sa.Column('contract_id', sa.Integer(), nullable=False),
    sa.Column('support_contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contract_id'], ['contract_table.id'], ),
    sa.ForeignKeyConstraint(['support_contact_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_table')
    op.drop_table('contract_table')
    op.drop_table('customer_table')
    op.drop_table('user_table')
    op.drop_table('team_table')
    # ### end Alembic commands ###