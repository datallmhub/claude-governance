Generate a complete feature slice for the domain: $ARGUMENTS

Follow all rules in .claude/rules/frontend.md.

Generate these files:

1. `src/types/[name].ts`
   - TypeScript interface with proper typing (no any, no id: number — use uid: string)

2. `src/api/[plural].api.ts`
   - API functions using the configured apiClient
   - Typed return values

3. `src/hooks/use[Name]s.ts`
   - TanStack Query hooks: `use[Name]s()` list + `use[Name](uid)` detail
   - Typed: `useQuery<[Name][], ApiError>`

4. `src/components/[Name]Card.tsx`
   - shadcn/ui components only
   - Handles all required props via typed interface

5. `src/pages/[Name]ListPage.tsx`
   - Orchestration only: calls hooks, renders components
   - Handles isLoading and isError states explicitly
