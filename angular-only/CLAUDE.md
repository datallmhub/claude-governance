# [Project Name] — Claude Code Governance

## Project Overview

[Brief description — what this app does, who uses it, what value it delivers.]

- **Type**: Single-Page Application (Angular / TypeScript)
- **Users**: [target users]
- **Model**: [SPA consuming external APIs / BFF / etc.]

---

## Tech Stack

| Component     | Technology                    |
|---------------|-------------------------------|
| Framework     | Angular 18 (standalone)       |
| Language      | TypeScript 5 (strict)         |
| CLI           | Angular CLI 18                |
| UI Components | Angular Material 18           |
| State         | NgRx Signals / NgRx Store     |
| Reactive      | RxJS 7                        |
| Routing       | Angular Router                |
| Forms         | Reactive Forms + Zod          |
| Tests         | Jest + Angular Testing Library|
| E2E           | Cypress / Playwright          |

---

## Directory Architecture

```
src/app/
├── core/              # Singleton services, guards, interceptors, app config
├── shared/            # Reusable components, directives, pipes
├── features/          # Feature modules (one folder per domain)
│   └── [feature]/
│       ├── components/
│       ├── services/
│       ├── store/
│       └── [feature].routes.ts
└── layout/            # Shell components (header, sidebar, footer)
```

**Rules:**
- Always use standalone components — no `NgModule` unless required by a third-party lib.
- `core/` services are provided in `root`. Never in a component.
- `shared/` contains only presentational, stateless components.
- `features/` are lazy-loaded via the router.

---

## Development Rules

- Always use the `inject()` function instead of constructor injection.
- Always use `OnPush` change detection on all components.
- Always unsubscribe with `takeUntilDestroyed()` or the `async` pipe.
- Always use Reactive Forms — never Template-driven Forms for complex forms.
- Always use typed `HttpClient` responses: `http.get<Product[]>(url)`.

---

## Commands

```bash
ng serve             # Start dev server (localhost:4200)
ng build             # Production build
ng test              # Unit tests (Jest)
ng e2e               # E2E tests (Cypress)
npm run typecheck    # tsc --noEmit
npm run lint         # ESLint
```

---

## Known Constraints

- [API base URL, auth mechanism, interceptors in place]
- [Angular version compatibility constraints]
- [Browser compatibility requirements]
