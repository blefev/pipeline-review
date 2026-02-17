from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Shot, ShotStatus
from app.schemas import ShotCreate, ShotDetail, ShotRead, ShotUpdate

router = APIRouter(prefix="/shots", tags=["shots"])


@router.get("", response_model=list[ShotRead])
def list_shots(
    sequence_id: int | None = Query(None),
    status: ShotStatus | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Shot)
    if sequence_id is not None:
        q = q.filter(Shot.sequence_id == sequence_id)
    if status is not None:
        q = q.filter(Shot.status == status)
    return q.order_by(Shot.id).all()


@router.post("", response_model=ShotRead, status_code=201)
def create_shot(payload: ShotCreate, db: Session = Depends(get_db)):
    shot = Shot(**payload.model_dump())
    db.add(shot)
    db.commit()
    db.refresh(shot)
    return shot


@router.get("/{shot_id}", response_model=ShotDetail)
def get_shot(shot_id: int, db: Session = Depends(get_db)):
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if not shot:
        raise HTTPException(404, "Shot not found")
    return shot


@router.patch("/{shot_id}", response_model=ShotRead)
def update_shot(shot_id: int, payload: ShotUpdate, db: Session = Depends(get_db)):
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if not shot:
        raise HTTPException(404, "Shot not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(shot, field, value)
    db.commit()
    db.refresh(shot)
    return shot
