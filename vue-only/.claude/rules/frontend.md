---
paths:
  - src/**/*.vue
  - src/**/*.ts
---

# Frontend Rules — Vue 3 / TypeScript

## TypeScript

- Always use `<script setup lang="ts">` syntax. Never Options API or `<script>` without setup.
- Always use `unknown` + type guard instead of `any`.
- Always keep `strict: true` in `tsconfig.json`.

## Components

- Always use `defineProps<{ ... }>()` with TypeScript generics — never runtime props.
- Always use `defineEmits<{ eventName: [payload: Type] }>()` with typed events.
- Always name component files in PascalCase: `ProductCard.vue`.
- Always use `<template>` with a single root element or Fragment.

```vue
<script setup lang="ts">
const props = defineProps<{ product: Product }>();
const emit = defineEmits<{ select: [uid: string] }>();
</script>
```

## Composables

- Always prefix composable files and functions with `use`: `useProducts.ts` → `useProducts()`.
- Always place data fetching in composables, never directly in a component.
- Always return reactive refs from composables: `return { data, isLoading, error }`.

```typescript
// composables/useProducts.ts
export function useProducts() {
  const data = ref<Product[]>([]);
  const isLoading = ref(false);
  const error = ref<ApiError | null>(null);
  // ...
  return { data: readonly(data), isLoading, error };
}
```

## State Management (Pinia)

- Always define stores with `defineStore('name', () => { ... })` (setup syntax).
- Always use `storeToRefs()` when destructuring reactive properties from a store.
- Always keep server data out of stores — use composables for data fetching.
- Always name store files: `useProductStore.ts`.

## Forms

- Always use Vee-Validate + Zod for all forms.
- Always define the schema with Zod and pass it to `useForm({ validationSchema })`.
- Always display validation messages inline using `<ErrorMessage name="field" />`.

## Error Handling

- Always handle errors in composables — expose an `error` ref to the component.
- Always show user-facing errors with a global `useToast()` composable.
- Always use `<Suspense>` with an `<ErrorBoundary>` wrapper for async components.

## Performance

- Always use `v-memo` only when profiler shows a real problem.
- Always use virtual scrolling (`vue-virtual-scroller`) for lists exceeding 100 items.
- Always lazy-load route components: `component: () => import('./pages/ProductList.vue')`.
