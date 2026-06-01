---
paths:
  - src/**/*.tsx
  - src/**/*.ts
---

# Frontend Rules — React / TypeScript

## TypeScript

- Always use `unknown` + type guard instead of `any`.
- Always declare shared types in `/types`. Inline types only for local component props.
- Always use `interface` for objects, `type` for unions and intersections.
- Always keep `strict: true` enabled in `tsconfig.json`.

## Components

- One component per file. PascalCase name, PascalCase.tsx filename.
- Always use shadcn/ui components (Button, Input, Dialog, etc.) for interactive elements.
- Always place page logic in custom hooks from `/hooks`. Pages only orchestrate.
- Always fetch data via a custom hook, never directly in a component.

```tsx
export function ProductListPage() {
  const { data, isLoading, isError } = useProducts();
  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage />;
  return <ProductList products={data} />;
}
```

## Data Fetching

- Always use TanStack Query for all server data fetching.
- Always place API functions in `/api`, one file per resource (`products.api.ts`).
- Always declare query keys as constants in `/api/query-keys.ts`.
- Always type query errors: `useQuery<Product[], ApiError>`.

```ts
// /api/products.api.ts
export const getProducts = (): Promise<Product[]> =>
  apiClient.get('/products').then(r => r.data);

// /hooks/useProducts.ts
export function useProducts() {
  return useQuery({ queryKey: ['products'], queryFn: getProducts });
}
```

## State Management

- Local state (form, modal): `useState` in the component.
- Shared state between nearby components: lift to parent or `useContext`.
- Global app state (current user, theme, notifications): Zustand store in `/store`.
- Always use TanStack Query for server data. Zustand holds client-only state.

## Forms

- Always use `react-hook-form` + `zod` for all forms.
- Always declare the Zod schema in the same file as the form.
- Always display validation messages inline below each field.

## Error Handling

- Always render an explicit error state when `isError` is true.
- Always use React `ErrorBoundary` for unexpected render errors.
- Always show a shadcn/ui `Toast` for mutation errors.

## Accessibility

- Always add `aria-label` to interactive elements whose visible content is an icon only.
- Always add a descriptive `alt` to images. Use `alt=""` for decorative images only.
- Always keep focus coherent after opening/closing a Dialog.

## Performance

- Always use `@tanstack/react-virtual` for lists exceeding 100 items.
- Always import Lucide icons by name: `import { Pencil } from 'lucide-react'`.
- Add `React.memo` only when the profiler shows a real problem, not preemptively.
