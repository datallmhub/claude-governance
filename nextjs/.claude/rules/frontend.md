---
paths:
  - src/app/**/*.tsx
  - src/components/**/*.tsx
  - src/hooks/**/*.ts
---

# Frontend Rules — Next.js Client Components

## Server vs Client Components

- Always default to Server Components. Add `'use client'` only when the component uses hooks, event handlers, or browser APIs.
- Always annotate `'use client'` at the top of the file — never mid-file.
- Always push `'use client'` boundaries as deep as possible (leaf components, not layouts).

```tsx
// Correct — Client Component only where interactivity is needed
'use client';
export function AddToCartButton({ productUid }: { productUid: string }) {
  const { mutate } = useAddToCart();
  return <Button onClick={() => mutate(productUid)}>Add to cart</Button>;
}
```

## TypeScript

- Always use `unknown` + type guard instead of `any`.
- Always keep `strict: true` in `tsconfig.json`.
- Always type Server Action return values with `ActionResult<T>` or similar.

## Components

- Always use shadcn/ui for interactive UI elements.
- Always place client logic in custom hooks from `/hooks`.
- Always use `use client` for any component using `useState`, `useEffect`, or event handlers.

## Data Fetching

- Server Components: always `fetch()` directly with `cache` and `revalidate` options.
- Client Components: always use TanStack Query — never raw `fetch` in `useEffect`.
- Always use `Suspense` boundaries around async Server Components.

```tsx
// Server Component — direct fetch
async function ProductList() {
  const products = await getProducts(); // server-side, cached
  return <ul>{products.map(p => <ProductCard key={p.uid} product={p} />)}</ul>;
}
```

## Forms & Mutations

- Always use Server Actions for form submissions and mutations.
- Always validate Server Action inputs with Zod before any DB operation.
- Always use `useFormState` + `useFormStatus` for progressive-enhancement forms.
- Always use `revalidatePath()` or `revalidateTag()` after a successful mutation.

## State Management

- Server state: Server Components + TanStack Query (client).
- Client-only state (UI, preferences): Zustand store.
- Always avoid storing server data in Zustand — use TanStack Query cache instead.

## Performance

- Always use `next/image` for all images — never raw `<img>` tags.
- Always use `next/link` for internal navigation — never raw `<a>` tags.
- Always use `loading.tsx` files for Suspense loading states at the route level.
- Always import Lucide icons by name: `import { Pencil } from 'lucide-react'`.
