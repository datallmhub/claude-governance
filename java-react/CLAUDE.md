# TaskFlow — Claude Code Governance

## Project Context

Multi-tenant SaaS — Spring Boot 3.3 / React 18.
Each organization is strictly isolated at the data level.
Developer level: see `dev-level.md`.

---

## CRITICAL — Non-negotiable

Violations here are bugs, not style issues.

- **Tenant isolation**: every repository query MUST filter by `organizationId`. Never query by entity ID alone.
- **organizationId source**: extract from JWT claims (security context) only. Never from request body, path variable, or query parameter.
- **Public IDs only**: use `publicId` (UUID) in all URLs and API responses. Never expose `id` (Long).
- **No secrets in code**: tokens, passwords, keys always via `@Value` or `@ConfigurationProperties`.
- **Flyway immutability**: never edit an existing migration. Always create a new versioned script.

---

## Backend Rules

**Architecture**
- `controller → service → repository`. No layer skipping.
- Controllers may: validate requests, map DTOs, extract auth context, call services.
- Controllers must not: access repositories, implement business rules, manage transactions.

**DTOs**
- Separate `*Request` and `*Response` records for every endpoint.
- Entities never leave the persistence layer — services expose DTOs only.
- Naming: `CreateTaskRequest`, `TaskResponse`, `UpdateTaskRequest`.

**Exceptions**
- All business exceptions extend `TaskFlowException`.
- Handled exclusively in `GlobalExceptionHandler`.

**Data access**
- Collection endpoints must return `Page<T>` or `Slice<T>`. Never unbounded `List<T>`.
- `FetchType.LAZY` on all `@OneToMany`. Use explicit JPQL fetch joins.
- Every `RestTemplate`/`WebClient`: 5s connect timeout, 30s read timeout.

**Authorization**
- Authentication does not imply authorization.
- Every service method accessing business data must verify ownership and permissions against the current organization and user.

**Correct repository signature example**
```java
Page<Task> findByProjectPublicIdAndOrganizationId(
    UUID projectPublicId, Long organizationId, Pageable pageable);
```

---

## Frontend Rules

- `unknown` + type guard — never `any`.
- Fetch logic in `/api` only — never inside a component or hook.
- shadcn/ui components everywhere — no raw HTML elements.
- Always handle `isLoading` and `isError` in data-fetching components.
- Global state → `/store`. Local state → component.

---

## Security Rules

**Validation**
- Backend: `@Valid` + Bean Validation at controller layer.
- Frontend: Zod + react-hook-form at form layer.

**Logging — never log**
`email`, `accessToken`, `refreshToken`, `password`, user full name.

**CORS**
- Dev: `localhost:5173`. Prod: `taskflow.app`. Never `allowedOrigins("*")`.

---

## Testing Rules

- Service layer: JUnit 5 + Mockito.
- Repository layer: Testcontainers integration tests.
- Every repository integration test must verify organization isolation (cross-tenant data must not be accessible).

---

## Modification Rules

| Situation | Action |
|-----------|--------|
| Change < 10 lines | Targeted diff only — never rewrite the full file |
| New DB change needed | New `V{n}__description.sql` — never edit existing migration |
| New file | Only if no existing file can be extended |

---

## Available Commands

| Command | Purpose |
|---------|---------|
| `/gov-check` | Audit current file against governance rules |
| `/security-review` | Security checklist on current file |
| `/scaffold <domain>` | Generate complete CRUD feature (entity, DTOs, service, controller, migration) |
| `/new-migration <description>` | Generate next Flyway migration script |

---

## Known Gotchas

- **JWT expiry**: access token = 15 min, refresh token = 7 days. Silent refresh handled by Axios interceptor in `/api/client.ts`. Do not add manual refresh logic elsewhere.
- **WebSocket**: real-time notifications use STOMP on `/ws`. Never mix with REST endpoints or add REST logic inside STOMP handlers.
- **Email**: notifications go through `@Async` jobs. Never call the mail service synchronously from a controller — it will block the request thread.
- **Flyway order**: migration FK constraints must respect table creation order. Always check dependencies before creating a new script.
- **Pagination**: task lists can exceed 10,000 rows. Never return unbounded `List<T>` from collection endpoints — always use `Page<T>` or `Slice<T>`.
- **CORS**: configured for `localhost:5173` (dev) and `taskflow.app` (prod) only. Never use `allowedOrigins("*")` in production.
