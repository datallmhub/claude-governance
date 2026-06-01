# Architecture — React SPA Overview

## System Diagram

```
┌──────────────────────────────────────────┐
│           BROWSER (React SPA)            │
│   React 18 + TypeScript (Vite / Vercel)  │
│                                          │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │  Pages   │→ │  Hooks   │→ │  API   │ │
│  │(routing) │  │(logic)   │  │(fetch) │ │
│  └──────────┘  └──────────┘  └───┬────┘ │
│                                  │      │
│  ┌───────────────────────────────┘      │
│  │  TanStack Query (server state cache) │
│  └──────────────────────────────────────│
│  ┌──────────────────────────────────────│
│  │  Zustand (client state)              │
│  └──────────────────────────────────────│
└──────────────────────────────────────────┘
         │ HTTPS REST / GraphQL
┌────────▼─────────────────────────────────┐
│        EXTERNAL API (backend)            │
│   Provided by another team / service     │
└──────────────────────────────────────────┘
```

## Key Decisions

### 1. TanStack Query for all server state
All data from external APIs is managed by TanStack Query. No manual `useEffect` + `useState` for fetching.
**Impact**: `store/` never holds server data. Mutations always call `invalidateQueries` after success.

### 2. Zustand for client-only state
Only truly client-side state (current user preferences, UI state, cart) lives in Zustand stores.
**Impact**: stores are small and fast. Server data is never duplicated.

### 3. Pages orchestrate, hooks own logic
Pages contain no business logic — they call hooks and render. All logic lives in `/hooks`.
**Impact**: easy to test in isolation, reusable across pages.

## Data Flow

```
User action
    → Component event handler
    → Hook (useMutation / useQuery)
    → api/ function
    → External API
    → TanStack Query cache update
    → Component re-renders
```
