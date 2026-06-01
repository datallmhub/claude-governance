# Architecture — Angular SPA Overview

## System Diagram

```
┌──────────────────────────────────────────────┐
│             BROWSER (Angular SPA)             │
│       Angular 18 + TypeScript (Vercel)        │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Features │→ │ Services │→ │ HttpClient │  │
│  │(lazy)    │  │(root)    │  │+ Intercept │  │
│  └──────────┘  └──────────┘  └─────┬──────┘  │
│                                    │         │
│  ┌─────────────────────────────────┘         │
│  │  NgRx Signals / NgRx Store (state)        │
│  └───────────────────────────────────────────│
└──────────────────────────────────────────────┘
         │ HTTPS REST
┌────────▼──────────────────────────────────────┐
│            EXTERNAL API (backend)             │
└───────────────────────────────────────────────┘
```

## Key Decisions

### 1. Standalone components everywhere
No NgModule declarations. All components are `standalone: true`.
**Impact**: smaller bundles, simpler dependency tree, direct `import` of what you use.

### 2. OnPush change detection by default
Every component uses `ChangeDetectionStrategy.OnPush`.
**Impact**: Angular only checks components when inputs change or an Observable emits. Major performance gain.

### 3. Feature-based structure with lazy loading
Each domain (products, orders, auth) lives in `features/` and is lazy-loaded via the router.
**Impact**: initial bundle stays small. Features are isolated and independently deployable.

### 4. inject() over constructor injection
`inject()` function used everywhere instead of constructor injection.
**Impact**: simpler class declarations, works in functional guards and resolvers.

## Data Flow

```
User action
    → Component event (OnPush boundary)
    → Service method (returns Observable)
    → HttpClient (with interceptors: auth, error handling)
    → External API
    → Observable emission → async pipe / toSignal()
    → Component re-renders
```
