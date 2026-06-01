# [Project Name] — Claude Code Governance

## Project Overview

[Brief description — what this app does, who uses it, what value it delivers.]

- **Type**: Full-stack Next.js application (App Router)
- **Users**: [target users]
- **Model**: [multi-tenant / SaaS / B2C / etc.]

---

## Tech Stack

### Full-stack
| Component     | Technology                  |
|---------------|-----------------------------|
| Framework     | Next.js 14 (App Router)     |
| Language      | TypeScript 5 (strict)       |
| Runtime       | Node.js 20                  |
| Auth          | NextAuth.js v5 (Auth.js)    |
| ORM           | Prisma 5                    |
| Database      | PostgreSQL 16               |
| Validation    | Zod                         |

### Frontend
| Component     | Technology               |
|---------------|--------------------------|
| UI Components | shadcn/ui + Tailwind CSS |
| Client state  | Zustand                  |
| Data fetching | TanStack Query v5 (client components) |
| Forms         | react-hook-form + Zod    |

### Testing & Infra
| Component     | Technology               |
|---------------|--------------------------|
| Unit tests    | Vitest + Testing Library |
| E2E tests     | Playwright               |
| Deploy        | Vercel                   |
| DB hosting    | Vercel Postgres / Neon   |

---

## Directory Architecture

```
src/
├── app/                   # App Router — layouts, pages, API routes
│   ├── (auth)/            # Route group: auth pages (login, register)
│   ├── (dashboard)/       # Route group: protected pages
│   ├── api/               # API route handlers (route.ts)
│   └── layout.tsx         # Root layout
│
├── components/            # Shared UI components (always Client or Server annotated)
├── lib/                   # Server-only utilities (db, auth, email)
│   ├── db.ts              # Prisma client singleton
│   └── auth.ts            # NextAuth configuration
├── actions/               # Server Actions (one file per domain)
├── hooks/                 # Client-side custom hooks
├── store/                 # Zustand stores (client state only)
├── types/                 # Shared TypeScript types
└── schemas/               # Zod schemas (shared between client and server)
```

**Rules:**
- Always mark components with `'use client'` explicitly when they use hooks or events.
- Server Components are the default — add `'use client'` only when required.
- Always use Server Actions for mutations — no API routes for form submissions.
- `lib/` is server-only — never import in Client Components.

---

## Development Rules

- Always validate with Zod at Server Action and API route boundaries.
- Always use Prisma transactions for multi-table writes.
- Always use `unstable_cache` or `revalidatePath` for cache invalidation.
- Always use `unknown` + type guard instead of `any`.
- Always store session tokens in `HttpOnly` cookies via NextAuth — never in `localStorage`.

---

## Commands

```bash
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build
npm run test         # Unit tests (Vitest)
npm run test:e2e     # E2E tests (Playwright)
npm run typecheck    # tsc --noEmit
npm run lint         # ESLint
npx prisma migrate dev    # Run DB migrations (dev)
npx prisma generate       # Regenerate Prisma client
npx prisma studio         # Open DB browser
```

---

## Known Constraints

- Server Components cannot use hooks, browser APIs, or event handlers.
- `'use server'` functions must be async — sync Server Actions are not supported.
- Prisma client must be instantiated as a singleton to avoid connection pool exhaustion.
- NextAuth session is available server-side via `auth()`, client-side via `useSession()`.
