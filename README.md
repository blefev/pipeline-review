# Pipeline Review

A full-stack VFX shot tracking and supervisor review application. Models the domain of a visual effects production: shows contain sequences, sequences contain shots, and shots receive supervisor review notes with full-text search.

## Screenshots

<!-- Add screenshots here, e.g.:
![Show list](docs/screenshots/show-list.png)
![Sequence detail with status pipeline](docs/screenshots/sequence-detail.png)
![Shot detail with reviews](docs/screenshots/shot-detail.png)
![Search results](docs/screenshots/search.png)
-->

## Quick Start

```bash
docker compose up --build
```

- **Frontend:** http://localhost:3000
- **API docs:** http://localhost:8000/docs

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

## Project Structure

```
pipeline-review-api/
├── app/                        # FastAPI backend
│   ├── main.py                 # App entry point, CORS, lifespan
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── search.py               # Elasticsearch indexing and search
│   ├── seed.py                 # Demo data seeder
│   ├── database.py             # Engine and session management
│   ├── config.py               # Environment settings
│   └── routers/                # Route handlers
│       ├── shows.py
│       ├── sequences.py
│       ├── shots.py
│       └── reviews.py
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── api/                # Fetch client + TypeScript interfaces
│   │   ├── hooks/              # TanStack Query hooks
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Route-level page components
│   │   └── styles/             # CSS custom properties, dark theme
│   ├── Dockerfile              # Multi-stage: node build → nginx serve
│   └── nginx.conf              # SPA fallback + /api/ reverse proxy
├── tests/                      # pytest suite (SQLite, no ES required)
├── alembic/                    # Database migrations
└── docker-compose.yml          # All 4 services
```

## Tech Stack

### Backend
- **Python 3.12** — FastAPI, SQLAlchemy 2.0, Pydantic v2
- **PostgreSQL 16** — relational data store
- **Elasticsearch 8.17** — full-text search on review notes

### Frontend
- **React 19** + **TypeScript** via Vite
- **TanStack Query v5** — data fetching with query key factories, optimistic updates, cache invalidation
- **React Router v7** — client-side routing
- **Plain CSS** with custom properties — dark theme matching VFX tooling

### Infrastructure
- **Docker Compose** — 4-service orchestration (frontend, API, PostgreSQL, Elasticsearch)
- **nginx:alpine** — serves the SPA, proxies `/api/` to the backend

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

## Architecture Decisions

- **SQLAlchemy mapped_column style** — modern declarative ORM syntax with full type hints
- **Pydantic v2 schemas** — request validation and response serialisation with `from_attributes` mode
- **Alembic migrations** — version-controlled schema changes (tables also auto-created on startup for convenience)
- **Elasticsearch graceful degradation** — search endpoints return empty results if ES is unavailable; the rest of the API continues to function
- **Seed data** — realistic VFX production data with actual supervisor review language (lighting, compositing, FX notes)
- **TanStack Query patterns** — query key factories, mutations with cache invalidation, optimistic updates on status changes, conditional queries for search
- **Dark theme** — matches VFX tooling conventions (Nuke, Maya, Houdini, ShotGrid)

## Running Tests

```bash
docker compose run api pytest
```

Tests use an in-memory SQLite database and do not require Elasticsearch.

## Configuration

All configuration is via environment variables. Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | _(empty)_ | Comma-separated allowed origins |
| `READ_ONLY` | `false` | Reject all non-GET requests with 403 |
| `SEED_ON_STARTUP` | `false` | Auto-seed if database is empty on boot |
| `POSTGRES_USER` | `pipeline` | Postgres username |
| `POSTGRES_PASSWORD` | `pipeline` | Postgres password |
| `POSTGRES_DB` | `pipeline` | Postgres database name |
| `FRONTEND_PORT` | `3000` | Host port for the frontend |
| `API_PORT` | `8000` | Host port for the API |
| `ES_JAVA_OPTS` | `-Xms256m -Xmx256m` | Elasticsearch JVM heap |

## Deploying as a Public Demo

```bash
cp .env.example .env
# Edit .env: set READ_ONLY=true, SEED_ON_STARTUP=true, CORS_ORIGINS, FRONTEND_PORT=80
docker compose up -d
```

With `SEED_ON_STARTUP=true`, the API auto-seeds on first boot if the database is empty. `READ_ONLY=true` then blocks all writes.
