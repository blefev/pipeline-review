import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ShotStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    review = "review"
    approved = "approved"
    final = "final"


class ReviewStatus(str, enum.Enum):
    approved = "approved"
    needs_revision = "needs_revision"
    note = "note"


class Show(Base):
    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    sequences: Mapped[list["Sequence"]] = relationship(back_populates="show", cascade="all, delete-orphan")


class Sequence(Base):
    __tablename__ = "sequences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    show: Mapped["Show"] = relationship(back_populates="sequences")
    shots: Mapped[list["Shot"]] = relationship(back_populates="sequence", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_sequences_show_id", "show_id"),
    )


class Shot(Base):
    __tablename__ = "shots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sequence_id: Mapped[int] = mapped_column(ForeignKey("sequences.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[ShotStatus] = mapped_column(
        Enum(ShotStatus), default=ShotStatus.pending
    )
    assigned_to: Mapped[str | None] = mapped_column(String(100))
    frame_start: Mapped[int] = mapped_column(Integer, default=1001)
    frame_end: Mapped[int] = mapped_column(Integer, default=1100)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    sequence: Mapped["Sequence"] = relationship(back_populates="shots")
    reviews: Mapped[list["Review"]] = relationship(back_populates="shot", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_shots_sequence_id", "sequence_id"),
        Index("ix_shots_status", "status"),
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shot_id: Mapped[int] = mapped_column(ForeignKey("shots.id"), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[ReviewStatus] = mapped_column(Enum(ReviewStatus), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    department: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    shot: Mapped["Shot"] = relationship(back_populates="reviews")

    __table_args__ = (
        Index("ix_reviews_shot_id", "shot_id"),
    )
