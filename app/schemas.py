from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import ReviewStatus, ShotStatus


# --- Show ---

class ShowCreate(BaseModel):
    title: str
    code: str
    status: str = "active"


class ShowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    code: str
    status: str
    created_at: datetime


class ShowDetail(ShowRead):
    sequences: list["SequenceRead"] = []


# --- Sequence ---

class SequenceCreate(BaseModel):
    show_id: int
    code: str
    description: str | None = None


class SequenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    show_id: int
    code: str
    description: str | None
    created_at: datetime


class SequenceDetail(SequenceRead):
    shots: list["ShotRead"] = []


# --- Shot ---

class ShotCreate(BaseModel):
    sequence_id: int
    code: str
    status: ShotStatus = ShotStatus.pending
    assigned_to: str | None = None
    frame_start: int = 1001
    frame_end: int = 1100


class ShotUpdate(BaseModel):
    status: ShotStatus | None = None
    assigned_to: str | None = None
    frame_start: int | None = None
    frame_end: int | None = None


class ShotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sequence_id: int
    code: str
    status: ShotStatus
    assigned_to: str | None
    frame_start: int
    frame_end: int
    created_at: datetime
    updated_at: datetime


class ShotDetail(ShotRead):
    reviews: list["ReviewRead"] = []


# --- Review ---

class ReviewCreate(BaseModel):
    author: str
    status: ReviewStatus
    body: str
    department: str | None = None


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    shot_id: int
    author: str
    status: ReviewStatus
    body: str
    department: str | None
    created_at: datetime


class ReviewSearchResult(BaseModel):
    id: int
    shot_id: int
    author: str
    status: str
    body: str
    department: str | None
    score: float
