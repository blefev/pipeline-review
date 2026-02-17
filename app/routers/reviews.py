from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Review, Shot
from app.schemas import ReviewCreate, ReviewRead, ReviewSearchResult
from app.search import index_review, search_reviews

router = APIRouter(tags=["reviews"])


@router.get("/shots/{shot_id}/reviews", response_model=list[ReviewRead])
def list_reviews(shot_id: int, db: Session = Depends(get_db)):
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if not shot:
        raise HTTPException(404, "Shot not found")
    return (
        db.query(Review)
        .filter(Review.shot_id == shot_id)
        .order_by(Review.id)
        .all()
    )


@router.post("/shots/{shot_id}/reviews", response_model=ReviewRead, status_code=201)
def create_review(
    shot_id: int, payload: ReviewCreate, db: Session = Depends(get_db)
):
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if not shot:
        raise HTTPException(404, "Shot not found")
    review = Review(shot_id=shot_id, **payload.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    index_review(review)
    return review


@router.get("/search/reviews", response_model=list[ReviewSearchResult])
def search_reviews_endpoint(q: str = Query(..., min_length=1)):
    return search_reviews(q)
