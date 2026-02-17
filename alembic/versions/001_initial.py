"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "shows",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("status", sa.String(50), server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sequences",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("show_id", sa.Integer, sa.ForeignKey("shows.id"), nullable=False),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_sequences_show_id", "sequences", ["show_id"])

    op.create_table(
        "shots",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sequence_id", sa.Integer, sa.ForeignKey("sequences.id"), nullable=False),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("status", sa.Enum("pending", "in_progress", "review", "approved", "final", name="shotstatus"), server_default="pending"),
        sa.Column("assigned_to", sa.String(100)),
        sa.Column("frame_start", sa.Integer, server_default="1001"),
        sa.Column("frame_end", sa.Integer, server_default="1100"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_shots_sequence_id", "shots", ["sequence_id"])
    op.create_index("ix_shots_status", "shots", ["status"])

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("shot_id", sa.Integer, sa.ForeignKey("shots.id"), nullable=False),
        sa.Column("author", sa.String(100), nullable=False),
        sa.Column("status", sa.Enum("approved", "needs_revision", "note", name="reviewstatus"), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("department", sa.String(50)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_reviews_shot_id", "reviews", ["shot_id"])


def downgrade() -> None:
    op.drop_table("reviews")
    op.drop_table("shots")
    op.drop_table("sequences")
    op.drop_table("shows")
    op.execute("DROP TYPE IF EXISTS shotstatus")
    op.execute("DROP TYPE IF EXISTS reviewstatus")
