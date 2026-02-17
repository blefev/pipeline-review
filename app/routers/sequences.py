from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Sequence
from app.schemas import SequenceCreate, SequenceDetail, SequenceRead

router = APIRouter(prefix="/sequences", tags=["sequences"])


@router.get("", response_model=list[SequenceRead])
def list_sequences(
    show_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Sequence)
    if show_id is not None:
        q = q.filter(Sequence.show_id == show_id)
    return q.order_by(Sequence.id).all()


@router.post("", response_model=SequenceRead, status_code=201)
def create_sequence(payload: SequenceCreate, db: Session = Depends(get_db)):
    seq = Sequence(**payload.model_dump())
    db.add(seq)
    db.commit()
    db.refresh(seq)
    return seq


@router.get("/{sequence_id}", response_model=SequenceDetail)
def get_sequence(sequence_id: int, db: Session = Depends(get_db)):
    seq = (
        db.query(Sequence)
        .options(joinedload(Sequence.shots))
        .filter(Sequence.id == sequence_id)
        .first()
    )
    if not seq:
        raise HTTPException(404, "Sequence not found")
    return seq
