# [Project Name] — Claude Code Governance

## Project Overview

[Brief description — what this app does, who uses it, what value it delivers.]

- **Type**: Single-Page Application (React / TypeScript)
- **Users**: [target users]
- **Model**: [SPA consuming external APIs / BFF / etc.]

---

## Tech Stack

| Component     | Technology               |
|---------------|--------------------------|
| Framework     | React 18                 |
| Language      | TypeScript 5 (strict)    |
| Bundler       | Vite 5                   |
| UI Components | shadcn/ui + Tailwind CSS |
| Global state  | Zustand                  |
| Data fetching | TanStack Query v5        |
| Routing       | React Router v6          |
| Forms         | react-hook-form + Zod    |
| Tests         | Vitest + Testing Library |
| API mocking   | MSW v2                   |

---

## Directory Architecture

```
src/
├── components/        # Reusable UI components
├── pages/             # One component per route — orchestration only
├── hooks/             # Custom React hooks (data fetching, logic)
├── store/             # Zustand stores (global client state only)
├── api/               # API client functions + query keys
├── types/             # Shared TypeScript interfaces and types
└── lib/               # Pure utility functions
```

**Rules:**
- `pages/` orchestrate — no logic, no direct fetch.
- `hooks/` own data fetching and business logic.
- `store/` holds client-only state — never server data.
- `api/` is the only place that calls external services.

---

## Development Rules

- Always use `unknown` + type guard instead of `any`.
- Always use shadcn/ui components for interactive elements.
- Always use TanStack Query for all server data fetching.
- Always handle `isLoading` and `isError` states explicitly.
- Always store JWT tokens in memory, never in `localStorage`.

---

## Commands

```bash
npm run dev          # Start dev server (localhost:5173)
npm run build        # Production build
npm run test         # Run tests
npm run typecheck    # Type check (tsc --noEmit)
npm run lint         # Lint
npm run preview      # Preview production build
```

---

## Known Constraints

- [API base URL, auth mechanism]
- [Rate limits on external APIs]
- [Browser compatibility requirements]
