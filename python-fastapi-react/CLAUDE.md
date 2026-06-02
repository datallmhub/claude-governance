# [Project Name] — Claude Code Governance

## Project Overview

[Brief description — what this app does, who uses it, what value it delivers.]

- **Target users**: [target users]
- **Value**: [core value proposition]
- **Model**: [multi-tenant / SaaS / B2C / etc.]

---

## Tech Stack

### Backend
| Component    | Technology                        |
|--------------|-----------------------------------|
| Runtime      | Python 3.11                       |
| Framework    | FastAPI 0.111                     |
| Validation   | Pydantic v2                       |
| ORM          | SQLAlchemy 2.0 (async)            |
| Database     | PostgreSQL 16                     |
| Migrations   | Alembic                           |
| Auth         | python-jose (JWT) + passlib/bcrypt|
| Tests        | pytest + httpx + pytest-asyncio   |

### Frontend
| Component    | Technology               |
|--------------|--------------------------|
| Framework    | React 18                 |
| Language     | TypeScript 5 (strict)    |
| Bundler      | Vite 5                   |
| UI           | shadcn/ui + Tailwind CSS |
| State        | Zustand                  |
| Fetching     | TanStack Query v5        |
| Routing      | React Router v6          |
| Forms        | react-hook-form + Zod    |
| Tests        | Vitest + Testing Library |

### Infrastructure
- Docker + Docker Compose (local dev)
- CI/CD: GitHub Actions
- Deploy: Railway (backend) + Vercel (frontend)

---

## Directory Architecture

```
project/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app + router registration
│   │   ├── config.py           # Settings (pydantic-settings)
│   │   ├── database.py         # SQLAlchemy async engine + session
│   │   ├── routers/            # APIRouter per domain
│   │   ├── schemas/            # Pydantic request/response models
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── services/           # Business logic
│   │   ├── dependencies/       # FastAPI Depends() (auth, db session)
│   │   └── exceptions/         # Custom exceptions + handlers
│   ├── alembic/                # Alembic env + migration scripts
│   └── tests/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       ├── store/
│       ├── api/
│       ├── types/
│       └── lib/
│
└── infra/
    └── docker-compose.yml
```

**Golden rule**: `router → service → repository (SQLAlchemy)`. No layer skipping.

---

## Development Rules

### Backend
- Always use `public_id: UUID` in API paths and responses. Never expose internal integer IDs.
- Always use Pydantic schemas for request/response. Never return SQLAlchemy models directly.
- Always inject the DB session via `Depends(get_db)`. Never instantiate sessions manually.
- Always use `async def` for route handlers and service methods.
- Always raise `HTTPException` with explicit status codes for business errors.

### Frontend
- Always use `unknown` + type guard instead of `any`.
- Always use TanStack Query for all server data fetching.
- Always use shadcn/ui components for interactive elements.
- Always handle `isLoading` and `isError` states explicitly.

---

## Commands

### Backend
```bash
cd backend
uvicorn app.main:app --reload        # Start dev server (localhost:8000)
pytest                               # Run tests
pytest --cov=app tests/              # Coverage report
alembic upgrade head                 # Apply migrations
alembic revision --autogenerate -m "description"  # New migration
```

### Frontend
```bash
cd frontend
npm run dev          # Start dev server (localhost:5173)
npm run build        # Production build
npm run test         # Tests
npm run typecheck    # Type check
npm run lint         # Lint
```

### Infrastructure
```bash
docker compose up -d                            # Start full environment
docker compose down -v && docker compose up -d  # Reset database
```

---

## Known Constraints

- FastAPI auto-generates OpenAPI docs at `/docs` (Swagger) and `/redoc`.
- SQLAlchemy async sessions must be closed after each request — handled by `get_db` dependency.
- Alembic `autogenerate` does not detect all changes (e.g. check constraints) — always review generated scripts.
- JWT access tokens expire after **15 minutes**, refresh tokens after **7 days**.
- CORS configured for `localhost:5173` in dev and your production domain in prod.
