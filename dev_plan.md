# Pipeline Review API — Development Plan

## Context

Code sample for a Senior IT Software Engineer role at Weta FX. Demonstrates proficiency in Python, PostgreSQL, Elasticsearch, and Docker by modelling a realistic VFX pipeline domain: tracking shots through production and managing supervisor review notes.

The goal is clean, readable code in a containerised, run-with-one-command project that a hiring manager can clone, `docker compose up`, and immediately explore via FastAPI's interactive docs.

## Tech Stack

- **Python 3.12** (FastAPI, SQLAlchemy, Pydantic v2) — `python:3.12-alpine`
- **PostgreSQL 16** — `postgres:16-alpine`
- **Elasticsearch 8.17** — official image
- **Docker Compose** — orchestrates all services

## Data Model

```
Show (id, title, code, status, created_at)
  └── Sequence (id, show_id FK, code, description, created_at)
        └── Shot (id, sequence_id FK, code, status, assigned_to, frame_start, frame_end, created_at, updated_at)
              └── Review (id, shot_id FK, author, status, body, department, created_at)
```

- Shot statuses: `pending`, `in_progress`, `review`, `approved`, `final`
- Review statuses: `approved`, `needs_revision`, `note`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/shows` | List/create shows |
| GET | `/shows/{id}` | Get show with sequences |
| GET/POST | `/sequences` | List/create sequences (filter by show) |
| GET | `/sequences/{id}` | Get sequence with shots |
| GET/POST | `/shots` | List/create shots (filter by sequence, status) |
| GET/PATCH | `/shots/{id}` | Get/update shot |
| GET/POST | `/shots/{id}/reviews` | List/create reviews for a shot |
| GET | `/search/reviews?q=` | Full-text search reviews via Elasticsearch |
| POST | `/seed` | Populate database with demo VFX data |

## Implementation Phases

### Phase 1: Scaffold
- Directory structure, Dockerfile, docker-compose.yml, requirements.txt
- Minimal FastAPI app with health endpoint and Pydantic Settings config

### Phase 2: Database Layer
- SQLAlchemy engine, session, declarative base
- ORM models with relationships, indexes, and constraints
- Alembic migration configuration and initial migration

### Phase 3: API Endpoints
- Pydantic request/response schemas
- CRUD routers for shows, sequences, shots, and reviews
- Filtering support (by show, sequence, status)

### Phase 4: Elasticsearch Integration
- ES client with index management and graceful degradation
- Review indexing on creation
- Full-text search endpoint

### Phase 5: Seed Data
- Realistic VFX production data (shows, sequences, shots, review notes)
- POST /seed endpoint with auto-indexing into Elasticsearch

### Phase 6: Tests
- SQLite in-memory test database
- Tests for shows, shots, and reviews CRUD operations

### Phase 7: Documentation
- README with quick start, domain model, and API reference
- This development plan for transparency
