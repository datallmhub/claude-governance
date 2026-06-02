Review the current file or selection against the project governance rules.

Load and apply .claude/rules/backend.md, .claude/rules/frontend.md, and .claude/rules/database.md as appropriate for the file type.

Check for:

**Architecture**
- Layer skipping (controller calling repository directly)
- Business logic in controllers or repositories
- Direct JPA entity returned from controller

**Naming**
- Classes not following XxxController / XxxService / XxxRepository / XxxEntity suffixes
- DTOs not named CreateXxxRequest / XxxResponse
- Methods not using typed generics

**Code conventions**
- Raw types (List without generic, Map untyped)
- Missing @Valid on @RequestBody
- Missing @Transactional on service class
- FetchType.EAGER on @OneToMany or @ManyToMany
- any type in TypeScript
- fetch or useEffect used for data fetching instead of TanStack Query
- Raw HTML elements instead of shadcn/ui components

**Completeness**
- isLoading / isError not handled in React components
- No timeout configured on WebClient / RestTemplate calls

Report each violation with:
- File and line reference
- The violated rule
- A concrete fix suggestion
