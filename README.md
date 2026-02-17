# Pipeline Review API

A VFX shot tracking and supervisor review pipeline, built with FastAPI, PostgreSQL, and Elasticsearch.

Models the domain of a visual effects production: shows contain sequences, sequences contain shots, and shots receive supervisor review notes. Reviews are full-text indexed in Elasticsearch for instant search across production feedback.

## Quick Start

```bash
docker compose up --build
```

The API is available at **http://localhost:8000** with interactive docs at **http://localhost:8000/docs**.

Populate with demo data:

```bash
curl -X POST http://localhost:8000/seed
```

## Domain Model

```
Show (title, code, status)
  └── Sequence (code, description)
        └── Shot (code, status, assigned_to, frame_range)
              └── Review (author, status, body, department)
```

- **Shot statuses:** pending → in_progress → review → approved → final
- **Review statuses:** approved, needs_revision, note

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/shows` | List / create shows |
| GET | `/shows/{id}` | Show detail with sequences |
| GET/POST | `/sequences` | List / create sequences (filter by `show_id`) |
| GET | `/sequences/{id}` | Sequence detail with shots |
| GET/POST | `/shots` | List / create shots (filter by `sequence_id`, `status`) |
| GET/PATCH | `/shots/{id}` | Shot detail / update |
| GET/POST | `/shots/{id}/reviews` | List / create reviews |
| GET | `/search/reviews?q=` | Full-text search reviews via Elasticsearch |
| POST | `/seed` | Populate database with demo VFX data |
| GET | `/health` | Health check |

## Tech Stack

- **Python 3.12** — FastAPI, SQLAlchemy 2.0, Pydantic v2
- **PostgreSQL 16** — relational data store
- **Elasticsearch 8.17** — full-text search on review notes
- **Docker Compose** — single-command orchestration

## Architecture Decisions

- **SQLAlchemy mapped_column style** — modern declarative ORM syntax with full type hints
- **Pydantic v2 schemas** — request validation and response serialisation with `from_attributes` mode
- **Alembic migrations** — version-controlled schema changes (tables also auto-created on startup for convenience)
- **Elasticsearch graceful degradation** — search endpoints return empty results if ES is unavailable; the rest of the API continues to function
- **Seed data** — realistic VFX production data with actual supervisor review language (lighting, compositing, FX notes)

## Running Tests

```bash
docker compose run api pytest
```

Tests use an in-memory SQLite database and do not require Elasticsearch.
