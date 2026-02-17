from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base
from app.routers import reviews, sequences, shots, shows
from app.search import es_client, ensure_index
from app.seed import run_seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    await ensure_index()
    yield
    es_client.close()


app = FastAPI(
    title="Pipeline Review API",
    description="VFX shot tracking and supervisor review pipeline",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shows.router)
app.include_router(sequences.router)
app.include_router(shots.router)
app.include_router(reviews.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/seed", tags=["admin"])
def seed_database(db: Session = Depends(get_db)):
    counts = run_seed(db)
    return {"message": "Database seeded", **counts}
