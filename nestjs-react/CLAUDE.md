# TaskFlow — Claude Code Governance

## Project Context

Multi-tenant SaaS — NestJS 10 / React 18.
Each organization is strictly isolated at the data level.
Developer level: see `dev-level.md`.

---

## CRITICAL — Non-negotiable

Violations here are bugs, not style issues.

- **Tenant isolation**: every repository query MUST filter by `organizationId`. Never query by entity ID alone.
- **organizationId source**: extract from JWT claims via `@CurrentUser()` decorator only. Never from request body, path variable, or query parameter.
- **Public IDs only**: use `publicId` (UUID) in all URLs and API responses. Never expose internal `id` (integer).
- **No secrets in code**: tokens, passwords, keys always via `ConfigService`. Never `process.env` in services or controllers.
- **Migration immutability**: never edit an existing TypeORM migration. Always create a new timestamped script.

---

## Backend Rules

**Architecture**
- `controller → service → repository`. No layer skipping.
- One feature per NestJS module (`TasksModule`, `ProjectsModule`). Export services only through `exports`; import modules, never inject across module boundaries.
- Controllers may: validate DTOs, extract auth context, call services.
- Controllers must not: access repositories, implement business rules, map entities to responses.

**DTOs & validation**
- Separate `CreateXxxDto`, `UpdateXxxDto`, and `XxxResponseDto` for every endpoint.
- Always use `class-validator` + `class-transformer`. Never use raw `@Body()` without a typed DTO.
- Entities never leave the persistence layer — services expose DTOs only.

**NestJS patterns**
- Always use `@Injectable()` services injected via constructor. Never `new Service()`.
- Always register a global `ValidationPipe` with `whitelist: true` and `forbidNonWhitelisted: true`.
- Always use `@UseGuards(JwtAuthGuard)` on protected routes. Use `@Roles()` + `RolesGuard` for authorization.
- Always map responses in a `TransformInterceptor` or dedicated mapper — never in controllers.

**Exceptions**
- All business exceptions extend `DomainException` with an `ErrorCode` enum.
- Handled exclusively in `AllExceptionsFilter` (`@Catch()`).

**Data access**
- Collection endpoints must return paginated results (`PaginatedResponseDto<T>`). Never unbounded arrays.
- Always use typed `Repository<Entity>` (TypeORM) or the Prisma generated client. Never raw SQL without parameterization.

**Correct repository signature example**
```typescript
findByProjectPublicIdAndOrganizationId(
  projectPublicId: string,
  organizationId: number,
  options: IPaginationOptions,
): Promise<Pagination<TaskEntity>>;
```

---

## Frontend Rules

- `unknown` + type guard — never `any`.
- Fetch logic in `/api` only — never inside a component or hook body beyond calling API functions.
- shadcn/ui components everywhere — no raw HTML elements for interactive UI.
- Always handle `isLoading` and `isError` in data-fetching components.
- Global state → `/store`. Server state → TanStack Query only.

---

## Security Rules

**Validation**
- Backend: global `ValidationPipe` + `class-validator` on all DTOs.
- Frontend: Zod + react-hook-form at form layer.

**Logging — never log**
`email`, `accessToken`, `refreshToken`, `password`, user full name.

**CORS**
- Dev: `localhost:5173`. Prod: `taskflow.app`. Never `origin: true` or wildcard in production.

---

## Testing Rules

- Service layer: Jest unit tests with mocked repositories.
- Controller layer: `@nestjs/testing` + Supertest e2e per module.
- Repository layer: Testcontainers PostgreSQL integration tests.
- Every repository integration test must verify organization isolation (cross-tenant data must not be accessible).

---

## Modification Rules

| Situation | Action |
|-----------|--------|
| Change < 10 lines | Targeted diff only — never rewrite the full file |
| New DB change needed | New TypeORM migration — never edit existing migration |
| New file | Only if no existing file can be extended |

---

## Cost Optimization

Model switching is manual. Suggest `/model` when the task warrants it:

| Task type | Suggestion |
|-----------|------------|
| Docs, renaming, simple syntax fixes | Suggest `/model claude-haiku-4-5` |
| Feature dev, bug fix, architecture (default) | Stay on `claude-sonnet-4-6` |
| Blocked after 2 attempts, security review | Suggest `/model claude-opus-4-8` |

- If stuck after 2 failed attempts on the same problem: stop and tell the user to run `/model claude-opus-4-8`.
- Never suggest haiku for tasks involving entities, migrations, security, or multi-tenancy.

---

## Available Commands

| Command | Purpose |
|---------|---------|
| `/gov-check` | Audit current file against governance rules |
| `/security-review` | Security checklist on current file |
| `/scaffold <domain>` | Generate complete CRUD feature (module, DTOs, service, controller, migration) |
| `/new-migration <description>` | Generate next TypeORM migration script |

---

## Known Gotchas

- **JWT expiry**: access token = 15 min, refresh token = 7 days. Silent refresh handled by Axios interceptor in `/api/client.ts`. Do not add manual refresh logic elsewhere.
- **Global pipes**: `ValidationPipe` is registered once in `main.ts`. Do not add per-route validation pipes unless transforming groups.
- **Module imports**: if `TasksService` needs `ProjectsService`, import `ProjectsModule` in `TasksModule` — never import the service file directly across modules.
- **TypeORM migrations**: run `npm run migration:run` after every new migration. `synchronize: true` is forbidden in all environments except local scratch DBs.
- **Pagination**: task lists can exceed 10,000 rows. Never return unbounded arrays from collection endpoints.
- **CORS**: configured for `localhost:5173` (dev) and `taskflow.app` (prod) only.
