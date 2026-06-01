# Architecture — Vue 3 SPA Overview

## System Diagram

```
┌──────────────────────────────────────────────┐
│              BROWSER (Vue 3 SPA)             │
│        Vue 3 + TypeScript (Vite / Vercel)    │
│                                              │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐ │
│  │  Pages   │→ │Composables │→ │  api/    │ │
│  │(routing) │  │(logic)     │  │(fetch)   │ │
│  └──────────┘  └────────────┘  └────┬─────┘ │
│                                     │       │
│  ┌──────────────────────────────────┘       │
│  │  Pinia stores (client state)             │
│  └──────────────────────────────────────────│
└──────────────────────────────────────────────┘
         │ HTTPS REST
┌────────▼──────────────────────────────────────┐
│            EXTERNAL API (backend)             │
└───────────────────────────────────────────────┘
```

## Key Decisions

### 1. Composition API with `<script setup>` only
Options API is not used. All components use `<script setup lang="ts">`.
**Impact**: better TypeScript inference, smaller compiled output, consistent patterns.

### 2. Composables own data fetching and logic
Pages call composables. Composables call `/api`. Components render results.
**Impact**: logic is testable in isolation, reusable across pages.

### 3. Pinia for global client state
Server data stays in composables (reactive refs). Pinia holds only UI/session state.
**Impact**: stores are small and predictable. No server data duplication.

### 4. Vue Router with lazy-loaded routes
All routes use `() => import(...)` for code splitting.
**Impact**: initial bundle stays lean regardless of app size.

## Data Flow

```
User action
    → Component event handler (emits or calls composable method)
    → Composable (reactive ref mutation + API call)
    → api/ function
    → External API
    → Reactive ref update
    → Template re-renders via reactivity system
```
