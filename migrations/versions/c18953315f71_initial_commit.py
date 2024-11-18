"""initial commit

Revision ID: c18953315f71
Revises: 
Create Date: 2024-11-16 20:47:34.698629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c18953315f71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('vin', sa.String(), nullable=False),
    sa.Column('manafacturer_name', sa.String(), nullable=True),
    sa.Column('horse_power', sa.Integer(), nullable=True),
    sa.Column('model_name', sa.String(), nullable=True),
    sa.Column('model_year', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('fuel_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('vin')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    # ### end Alembic commands ###
