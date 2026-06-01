# TaskFlow — Claude Code Governance

## Project Overview

**TaskFlow** is a collaborative project management SaaS platform.
It lets teams create projects, manage tasks in real time, track progress,
and generate activity reports.

- **Target users**: product teams, developers, project managers
- **Value**: centralized task tracking with real-time notifications and automated reporting
- **Model**: multi-tenant — each organization is isolated at the data level

---

## Tech Stack

### Backend
| Component    | Technology                       |
|--------------|----------------------------------|
| Runtime      | Java 17                          |
| Framework    | Spring Boot 3.3                  |
| Security     | Spring Security 6 + JWT (JJWT)   |
| Persistence  | Spring Data JPA + Hibernate 6    |
| Database     | PostgreSQL 16                    |
| Migrations   | Flyway                           |
| Build        | Maven 3.9                        |
| Tests        | JUnit 5, Mockito, Testcontainers |

### Frontend
| Component    | Technology               |
|--------------|--------------------------|
| Framework    | React 18                 |
| Language     | TypeScript 5             |
| Bundler      | Vite 5                   |
| UI Components| shadcn/ui + Tailwind CSS |
| Global state | Zustand                  |
| Data fetching| TanStack Query v5        |
| Routing      | React Router v6          |
| Tests        | Vitest + Testing Library |

### Infrastructure
- Docker + Docker Compose (local dev)
- CI/CD: GitHub Actions
- Deploy: Railway (backend) + Vercel (frontend)

---

## Directory Architecture

```
taskflow/
├── backend/                    # Spring Boot application
│   └── src/
│       └── main/java/com/taskflow/
│           ├── config/         # Spring beans (Security, CORS, JPA)
│           ├── controller/     # REST controllers (@RestController)
│           ├── service/        # Business logic (@Service)
│           ├── repository/     # Data access (JpaRepository)
│           ├── domain/         # JPA entities + value objects
│           ├── dto/            # Transfer objects (Request/Response)
│           ├── exception/      # Business exceptions + global handler
│           └── security/       # JWT filter, UserDetails, AuthService
│
├── frontend/                   # React application
│   └── src/
│       ├── components/         # Reusable UI components
│       ├── pages/              # Pages (one per route)
│       ├── hooks/              # Custom React hooks
│       ├── store/              # Zustand stores
│       ├── api/                # HTTP clients (TanStack Query functions)
│       ├── types/              # Shared TypeScript types
│       └── lib/                # Pure utilities
│
└── infra/
    ├── docker-compose.yml
    └── migrations/             # Flyway scripts (V__description.sql)
```

**Golden rule**: each layer only talks to the layer directly below it.
`controller → service → repository`. No layer skipping.

---

## Development Rules

### Global
- Always use `public_id` (UUID) in URLs and API responses. Never expose internal sequential IDs.
- Always validate input at the system boundary (controllers on the backend, forms on the frontend).
- Always configure a timeout on every external HTTP call.
- Always sanitize logs: never include PII (emails, names, tokens).

### Backend
- Always use typed generics (`List<Task>`, not raw `List`).
- Controllers hold no business logic — delegate everything to the service.
- Always use distinct DTOs for Request and Response. Never expose a JPA entity directly.
- Always extend `TaskFlowException` for business exceptions, handled in `GlobalExceptionHandler`.
- Always place complex JPQL queries in the repository, never in the service.
- Always set timeouts on `RestTemplate` / `WebClient`: 5s connect, 30s read.

### Frontend
- Always use `unknown` + type guard instead of `any`.
- Always use shadcn/ui components instead of raw HTML elements.
- Always place fetch logic in `/api`, never directly in a component.
- Global state goes in `/store`. Local state stays in the component.
- Always handle `isLoading` and `isError` states in components that fetch data.

---

## Commands

### Backend
```bash
cd backend && mvn spring-boot:run     # Start backend
mvn clean package -DskipTests         # Full build
mvn test                              # Unit tests
mvn verify -Pintegration              # Integration tests (requires Docker)
mvn checkstyle:check                  # Linting
mvn jacoco:report                     # Coverage report
```

### Frontend
```bash
cd frontend && npm run dev            # Start frontend (dev)
npm run build                         # Production build
npm run test                          # Tests
npm run typecheck                     # Type check
npm run lint                          # Lint
```

### Infrastructure
```bash
docker compose up -d                                    # Start full environment
docker compose down -v && docker compose up -d postgres # Reset database
```

---

## Known Constraints & Gotchas

### Security
- JWT tokens expire after **15 minutes** (access) and **7 days** (refresh).
  The frontend handles silent refresh via the Axios interceptor in `/api/client.ts`.
- CORS is configured for `localhost:5173` in dev and `taskflow.app` in prod.
  Never use `allowedOrigins("*")` in production.

### Database
- The multi-tenant schema uses `organization_id` on all business tables.
  Every query must filter on `organization_id` — verify via integration tests.
- Flyway migrations are immutable. Always create a new script instead of editing an existing one.
- Migration order is critical: FK constraints must respect table creation order.

### Performance
- Task lists can exceed 10,000 rows. Always paginate with `Pageable`.
- Always use `FetchType.LAZY` on `@OneToMany` relations. Use explicit fetch joins.

### Misc
- WebSocket (real-time notifications) uses STOMP on `/ws`. Do not mix with REST endpoints.
- Email notifications go through an async job (`@Async`). Never call the mail service synchronously from a controller.
