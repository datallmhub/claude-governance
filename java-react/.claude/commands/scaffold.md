Generate a complete CRUD feature for the domain: $ARGUMENTS

Follow all rules in .claude/rules/backend.md, .claude/rules/database.md, and .claude/rules/frontend.md.

## Backend — generate these files:

1. `backend/src/main/java/com/[package]/[domain]/domain/[Name]Entity.java`
   - JPA entity with `public_id UUID`, `id BIGSERIAL`, audit fields
   - FetchType.LAZY on all relations, @Version for optimistic locking

2. `backend/src/main/java/com/[package]/[domain]/dto/Create[Name]Request.java`
   - Java record with Bean Validation annotations

3. `backend/src/main/java/com/[package]/[domain]/dto/[Name]Response.java`
   - Java record exposing `uid UUID` (mapped from public_id), never `id`

4. `backend/src/main/java/com/[package]/[domain]/repository/[Name]Repository.java`
   - JpaRepository with `findByPublicId(UUID)` method

5. `backend/src/main/java/com/[package]/[domain]/service/[Name]Service.java`
   - Interface with CRUD method signatures

6. `backend/src/main/java/com/[package]/[domain]/service/impl/[Name]ServiceImpl.java`
   - @Service @Transactional, readOnly on reads, throws typed exception if not found

7. `backend/src/main/java/com/[package]/[domain]/controller/[Name]Controller.java`
   - @RestController @RequestMapping("/api/v1/[plural]")
   - @PathVariable UUID, @Valid @RequestBody, ResponseEntity<T> with explicit status

8. `infra/migrations/V[TIMESTAMP]__create_[plural]_table.sql`
   - Includes public_id UUID DEFAULT gen_random_uuid(), indexes on public_id and org_id if multi-tenant

## Frontend — generate these files:

9. `frontend/src/types/[domain].ts`
   - TypeScript interface with `uid: string` (never `id: number`)

10. `frontend/src/api/[plural].api.ts`
    - API functions using apiClient, typed return values

11. `frontend/src/hooks/use[Name]s.ts`
    - TanStack Query hooks: `use[Name]s()` and `use[Name](uid)`

12. `frontend/src/components/[Name]Card.tsx`
    - shadcn/ui components only, handles isLoading/isError

13. `frontend/src/pages/[Name]ListPage.tsx`
    - Orchestration only — calls hooks, renders components
