"""Add file id column to params table

Revision ID: b9fd6bcd50e2
Revises: 8e44c2d99a18
Create Date: 2022-06-15 11:08:59.410835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b9fd6bcd50e2"
down_revision = "8e44c2d99a18"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("parameters", sa.Column("file_id", sa.Integer(), nullable=True))
    op.create_index(
        op.f("ix_parameters_file_id"), "parameters", ["file_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_parameters_file_id"), table_name="parameters")
    op.drop_column("parameters", "file_id")
    # ### end Alembic commands ###