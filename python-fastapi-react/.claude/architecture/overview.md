# Architecture — System Overview

## System Diagram

```
┌──────────────────────────────────────────────────┐
│              BROWSER (React SPA)                 │
│       React 18 + TypeScript (Vite / Vercel)      │
└─────────────────────┬────────────────────────────┘
                      │ HTTPS REST
┌─────────────────────▼────────────────────────────┐
│              BACKEND (FastAPI)                   │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Routers  │→ │ Services │→ │ Repositories │   │
│  │(FastAPI) │  │(Business)│  │(SQLAlchemy)  │   │
│  └──────────┘  └──────────┘  └──────┬───────┘   │
│                                     │           │
│  ┌──────────────────────────────────▼─────────┐ │
│  │         PostgreSQL 16                      │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  Auto-generated API docs: /docs (Swagger)        │
└──────────────────────────────────────────────────┘
```

## Key Architectural Decisions

### 1. Pydantic v2 for all I/O contracts
All request bodies and response payloads use Pydantic schemas. SQLAlchemy models are never returned directly.
**Impact**: every new endpoint needs a Request schema and a Response schema.

### 2. UUID public IDs
Internal integer PKs are never exposed. Every model has a `public_id UUID` used in all URLs and responses.
**Impact**: no IDOR risk. All `@router.get("/{uid}")` use `UUID` path parameters.

### 3. Async everywhere
FastAPI + SQLAlchemy 2.0 async. All route handlers, services, and repository methods use `async def`.
**Impact**: never mix sync and async code. Use `run_in_executor` for blocking operations.

### 4. Dependency injection via `Depends()`
DB sessions, current user, and services are injected via FastAPI's `Depends()` system.
**Impact**: never instantiate services or sessions manually inside route handlers.

### 5. Alembic for all schema changes
SQLAlchemy `create_all()` is never used in production. All schema changes go through Alembic.
**Impact**: every model change requires a new migration script.

## Application Modules

| Module         | Responsibility                    | Path                        |
|----------------|-----------------------------------|-----------------------------|
| `auth`         | Login, JWT, refresh tokens        | `app/routers/auth.py`       |
| `users`        | User management                   | `app/routers/users.py`      |
| `products`     | Product CRUD                      | `app/routers/products.py`   |
| `dependencies` | Shared Depends() (db, auth)       | `app/dependencies/`         |
| `models`       | SQLAlchemy ORM models             | `app/models/`               |
| `schemas`      | Pydantic request/response schemas | `app/schemas/`              |
