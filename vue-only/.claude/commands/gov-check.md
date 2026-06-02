Review the current file or selection against the project governance rules.

Load and apply .claude/rules/frontend.md.

Check for:

**TypeScript**
- any type used (should be unknown + type guard)
- Missing strict types on useQuery / useMutation
- Inline types that should be in /types

**Components**
- Fetch or useEffect used for data fetching (should use TanStack Query)
- Raw HTML elements instead of shadcn/ui (button, input, select...)
- Logic or fetch calls directly in a page component (should be in a hook)
- Missing isLoading / isError handling

**State**
- Server data stored in Zustand (should be in TanStack Query cache)
- Global state used for data that is local to one component

**Forms**
- Forms not using react-hook-form + zod
- Validation messages not displayed inline

**Performance**
- import * as Icons from 'lucide-react'

Report each violation with file, line, violated rule, and fix suggestion.
