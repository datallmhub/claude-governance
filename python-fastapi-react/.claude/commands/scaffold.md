Generate a complete CRUD feature for the domain: $ARGUMENTS

Follow all rules in .claude/rules/backend.md, .claude/rules/database.md, and .claude/rules/frontend.md.

## Backend — generate these files:

1. `backend/app/models/[name].py`
   - SQLAlchemy 2.0 model with `public_id UUID`, `id SERIAL`, audit fields

2. `backend/app/schemas/[name].py`
   - `Create[Name]Request(BaseModel)` with Field constraints
   - `[Name]Response(BaseModel)` exposing `uid: UUID` (from public_id), never `id`

3. `backend/app/repositories/[name]_repository.py`
   - Async methods: `find_by_public_id`, `find_all` (paginated), `save`, `soft_delete`

4. `backend/app/services/[name]_service.py`
   - Business logic, raises HTTPException for not found / conflicts
   - Injects repository via __init__

5. `backend/app/routers/[plural].py`
   - APIRouter with prefix="/api/v1/[plural]"
   - UUID path parameters, response_model declared, status_code explicit
   - Depends(get_current_user) on protected endpoints

6. Alembic migration
   - Run: `alembic revision --autogenerate -m "create_[plural]_table"`
   - Verify the generated script includes public_id and indexes

## Frontend — generate these files:

7. `frontend/src/types/[name].ts`
   - TypeScript interface with `uid: string`

8. `frontend/src/api/[plural].api.ts`
   - API functions using apiClient

9. `frontend/src/hooks/use[Name]s.ts`
   - TanStack Query hooks

10. `frontend/src/components/[Name]Card.tsx`
    - shadcn/ui only, handles isLoading/isError

11. `frontend/src/pages/[Name]ListPage.tsx`
    - Orchestration only
