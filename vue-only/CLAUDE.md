# [Project Name] — Claude Code Governance

## Project Overview

[Brief description — what this app does, who uses it, what value it delivers.]

- **Type**: Single-Page Application (Vue 3 / TypeScript)
- **Users**: [target users]
- **Model**: [SPA consuming external APIs / BFF / etc.]

---

## Tech Stack

| Component     | Technology               |
|---------------|--------------------------|
| Framework     | Vue 3 (Composition API)  |
| Language      | TypeScript 5 (strict)    |
| Bundler       | Vite 5                   |
| UI Components | Tailwind CSS + Headless UI|
| State         | Pinia                    |
| Routing       | Vue Router 4             |
| Utilities     | VueUse                   |
| Forms         | Vee-Validate + Zod       |
| Tests         | Vitest + Vue Testing Library |
| E2E           | Playwright               |

---

## Directory Architecture

```
src/
├── components/        # Reusable UI components (PascalCase.vue)
├── pages/             # Route components — orchestration only
├── composables/       # Reusable composition functions (use*.ts)
├── stores/            # Pinia stores (one per domain)
├── api/               # API client functions
├── types/             # Shared TypeScript types and interfaces
└── utils/             # Pure utility functions
```

**Rules:**
- Always use `<script setup lang="ts">` syntax.
- `pages/` orchestrate — no logic, no direct API calls.
- `composables/` own data fetching and reusable logic.
- `stores/` hold global client state — never cache server responses.

---

## Development Rules

- Always use `<script setup lang="ts">` — never Options API.
- Always use `defineProps<{...}>()` with TypeScript generics.
- Always use `defineEmits<{...}>()` with typed events.
- Always use Pinia stores with `storeToRefs()` to preserve reactivity.
- Always use `unknown` + type guard instead of `any`.

---

## Commands

```bash
npm run dev          # Start dev server (localhost:5173)
npm run build        # Production build
npm run test         # Unit tests (Vitest)
npm run test:e2e     # E2E tests (Playwright)
npm run typecheck    # vue-tsc --noEmit
npm run lint         # ESLint
```

---

## Known Constraints

- [API base URL, auth mechanism]
- [Vue 3 only — no Vue 2 patterns]
- [Browser compatibility requirements]
