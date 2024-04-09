"""
Initial migration.

Revision ID: 54c7cf343e1f
Revises:
Create Date: 2024-04-09 20:03:59.061322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "54c7cf343e1f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "modified",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "url",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("long", sa.String(), nullable=False),
        sa.Column("short", sa.String(), nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "modified",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "click",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("url_id", sa.Integer(), nullable=False),
        sa.Column("ip", sa.String(), nullable=False),
        sa.Column("user_agent", sa.String(), nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ),
        sa.ForeignKeyConstraint(["url_id"], ["url.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    op.drop_table("click")
    op.drop_table("url")
    op.drop_table("user")

