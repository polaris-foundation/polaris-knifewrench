"""empty message

Revision ID: 00bed7ede274
Revises: b979dd5e5b23
Create Date: 2019-11-13 09:50:20.633684

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "00bed7ede274"
down_revision = "b979dd5e5b23"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "amqp_message", sa.Column("message_raw_body", sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column("amqp_message", "message_raw_body")
