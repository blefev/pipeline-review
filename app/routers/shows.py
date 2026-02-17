from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Show
from app.schemas import ShowCreate, ShowDetail, ShowRead

router = APIRouter(prefix="/shows", tags=["shows"])


@router.get("", response_model=list[ShowRead])
def list_shows(db: Session = Depends(get_db)):
    return db.query(Show).order_by(Show.id).all()


@router.post("", response_model=ShowRead, status_code=201)
def create_show(payload: ShowCreate, db: Session = Depends(get_db)):
    show = Show(**payload.model_dump())
    db.add(show)
    db.commit()
    db.refresh(show)
    return show


@router.get("/{show_id}", response_model=ShowDetail)
def get_show(show_id: int, db: Session = Depends(get_db)):
    show = (
        db.query(Show)
        .options(joinedload(Show.sequences))
        .filter(Show.id == show_id)
        .first()
    )
    if not show:
        raise HTTPException(404, "Show not found")
    return show
