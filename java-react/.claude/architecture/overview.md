# Architecture — System Overview

## System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT                              │
│          React 18 + TypeScript (Vite / Vercel)          │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS REST + WebSocket (STOMP)
┌───────────────────────▼─────────────────────────────────┐
│                    BACKEND                               │
│           Spring Boot 3.3  (Railway)                    │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │
│  │ Controller │→ │  Service   │→ │    Repository      │ │
│  │ (REST API) │  │ (Business) │  │ (Spring Data JPA)  │ │
│  └────────────┘  └────────────┘  └─────────┬──────────┘ │
│                                             │            │
│  ┌──────────────────────────────────────────▼──────────┐ │
│  │          PostgreSQL 16  (Railway managed)           │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │  Async Layer : @Async jobs, WebSocket broker (STOMP) ││
│  └──────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Key Architectural Decisions

### 1. Column-based multi-tenancy (`org_id`)

All business tables carry `org_id`. Isolation is enforced at the application level (filter on every query). This choice simplifies deployment (single database) at the cost of strict DB-level isolation.

**Impact**: every new business entity must have `org_id`. Every repository must filter on `org_id`.

### 2. Stateless JWT authentication

No server-side session. The JWT contains `userId`, `orgId` and `roles`. `JwtAuthenticationFilter` populates the `SecurityContext` on every request.

**Impact**: token revocation is not immediate — requires a Redis blacklist (not yet implemented). Tokens expire in 15 min.

### 3. Strict frontend / backend separation

The frontend is a decoupled SPA. No server-side rendering (no Thymeleaf). The backend is a pure JSON API.

**Impact**: all frontend routes are client-side (React Router). The backend has no knowledge of UI routes.

### 4. WebSocket for real-time notifications

Real-time notifications (new comment, status change) go through STOMP over WebSocket. The broker is in-memory (no RabbitMQ in v1).

**Impact**: notifications do not survive a backend restart. Acceptable for v1.

### 5. Flyway-only schema evolution

The database schema evolves exclusively through Flyway. Hibernate neither generates nor modifies the schema (`ddl-auto: validate`).

**Impact**: every data model change requires a new SQL migration script.

---

## Application Modules

| Module         | Responsibility                              | Package                           |
|----------------|---------------------------------------------|-----------------------------------|
| `auth`         | Login, register, JWT, refresh token         | `com.taskflow.security`           |
| `organization` | Organization and member management          | `com.taskflow.organization`       |
| `project`      | Project CRUD, project members               | `com.taskflow.project`            |
| `task`         | Task CRUD, statuses, assignment             | `com.taskflow.task`               |
| `comment`      | Task comments                               | `com.taskflow.comment`            |
| `notification` | Real-time and email notifications           | `com.taskflow.notification`       |
| `report`       | Activity reports and statistics             | `com.taskflow.report`             |

---

## Authentication Flow

```
Client                    Backend                    DB
  │                          │                        │
  │── POST /auth/login ──────►│                        │
  │                          │── findByEmail ─────────►│
  │                          │◄── UserEntity ──────────│
  │                          │── validatePassword      │
  │◄── { accessToken,        │── generateTokens        │
  │      refreshToken }      │── saveRefreshToken ────►│
  │                          │                        │
  │── GET /api/v1/tasks ─────►│                        │
  │   Authorization: Bearer  │── validateJWT           │
  │                          │── extractOrgId          │
  │◄── [ tasks ] ────────────│── query with orgId ────►│
```
