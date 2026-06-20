# Architecture — System Overview

## System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT                              │
│          React 18 + TypeScript (Vite / Vercel)          │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS REST + WebSocket (Socket.io)
┌───────────────────────▼─────────────────────────────────┐
│                    BACKEND                               │
│           NestJS 10  (Railway / Render)                 │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │
│  │ Controller │→ │  Service   │→ │  Repository        │ │
│  │ (REST API) │  │ (Business) │  │ (TypeORM / Prisma) │ │
│  └────────────┘  └────────────┘  └─────────┬──────────┘ │
│                                             │            │
│  ┌──────────────────────────────────────────▼──────────┐ │
│  │          PostgreSQL 16  (managed)                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │  Cross-cutting: Guards, Pipes, Interceptors, Filters││
│  │  Async: Bull queues (@nestjs/bull), EventEmitter     ││
│  └──────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Key Architectural Decisions

### 1. Column-based multi-tenancy (`org_id`)

All business tables carry `org_id`. Isolation is enforced at the application level (filter on every query). This choice simplifies deployment (single database) at the cost of strict DB-level isolation.

**Impact**: every new business entity must have `organizationId`. Every repository query must filter on `organizationId`.

### 2. Stateless JWT authentication

No server-side session. The JWT contains `userId`, `organizationId`, and `roles`. `JwtAuthGuard` + `JwtStrategy` validate and attach the user on every request via `@CurrentUser()`.

**Impact**: token revocation is not immediate — requires a Redis blacklist (not yet implemented). Tokens expire in 15 min.

### 3. Strict frontend / backend separation

The frontend is a decoupled SPA. The backend is a pure JSON API with no view rendering.

**Impact**: all frontend routes are client-side (React Router). The backend has no knowledge of UI routes.

### 4. NestJS modular architecture

Each domain is a self-contained NestJS module with its own controller, service, entities, and DTOs. Shared infrastructure lives in `common/` (guards, filters, interceptors, decorators).

**Impact**: cross-module access goes through module `exports`/`imports` only. No direct service imports across feature folders.

### 5. TypeORM migration-only schema evolution

The database schema evolves exclusively through TypeORM migrations. `synchronize` is disabled in all persistent environments.

**Impact**: every data model change requires a new migration file with `up()` and `down()`.

### 6. WebSocket for real-time notifications

Real-time notifications (new comment, status change) go through `@nestjs/websockets` with Socket.io adapter. Auth via JWT at handshake.

**Impact**: notifications are ephemeral in v1 (in-memory adapter). Acceptable for MVP.

---

## Application Modules

| Module         | Responsibility                              | Path                              |
|----------------|---------------------------------------------|-----------------------------------|
| `AuthModule`   | Login, register, JWT, refresh token         | `src/modules/auth/`               |
| `OrganizationsModule` | Organization and member management   | `src/modules/organizations/`      |
| `ProjectsModule` | Project CRUD, project members             | `src/modules/projects/`           |
| `TasksModule`  | Task CRUD, statuses, assignment             | `src/modules/tasks/`              |
| `CommentsModule` | Task comments                             | `src/modules/comments/`           |
| `NotificationsModule` | Real-time and email notifications    | `src/modules/notifications/`      |

---

## Request Lifecycle

```
HTTP Request
    │
    ▼
Helmet + CORS middleware (main.ts)
    │
    ▼
Global ValidationPipe (strip unknown fields, transform DTOs)
    │
    ▼
JwtAuthGuard → JwtStrategy.validate() → @CurrentUser()
    │
    ▼
Controller method (typed DTO in, service call)
    │
    ▼
Service (business logic, orgId filter, domain exceptions)
    │
    ▼
Repository (TypeORM / Prisma parameterized query)
    │
    ▼
TransformInterceptor (entity → response DTO)
    │
    ▼
AllExceptionsFilter (uniform error body on failure)
```

---

## Authentication Flow

```
Client                    NestJS Backend              DB
  │                          │                        │
  │── POST /auth/login ──────►│                        │
  │                          │── findByEmail ─────────►│
  │                          │◄── UserEntity ──────────│
  │                          │── bcrypt.compare        │
  │◄── { accessToken,        │── sign JWT              │
  │      refreshToken }      │── saveRefreshToken ────►│
  │                          │                        │
  │── GET /api/v1/tasks ─────►│                        │
  │   Authorization: Bearer  │── JwtAuthGuard          │
  │                          │── extractOrgId          │
  │◄── [ tasks ] ────────────│── query with orgId ────►│
```
