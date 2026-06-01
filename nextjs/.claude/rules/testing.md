---
paths:
  - src/**/*.test.ts
  - src/**/*.test.tsx
  - tests/**/*.ts
  - e2e/**/*.ts
---

# Testing Rules — Next.js / Vitest / Playwright

## General Principles

- Always test one behavior per test.
- Always make tests independent of execution order.
- Always name tests to describe expected behavior.

## Server Components

- Always test Server Components with `render()` in an async context.
- Always mock `lib/db` and external services — never hit a real database in unit tests.
- Always mock `auth()` from NextAuth for authenticated components.

## Client Components

- Always use Testing Library with `renderWithProviders` wrapper (QueryClient + SessionProvider).
- Always use MSW to intercept API calls.
- Always select elements by accessible role or visible text.

## Server Actions

- Always test Server Actions as regular async functions — call them directly with mocked Prisma.
- Always test both the success path and the Zod validation error path.

```typescript
it('should return error when title is blank', async () => {
  const result = await createProduct({ title: '', price: 10 });
  expect(result.error).toContain('title');
});
```

## E2E Tests (Playwright)

- Always seed the database via Prisma in a `beforeAll` block.
- Always clean up test data in `afterAll`.
- Always run E2E tests against a local `next build && next start` — not the dev server.
- Always use `page.getByRole()` — never CSS selectors.

## Coverage

- Target minimum 70% on `/components`, `/hooks`, and `/actions`.
- Always exclude `app/**/layout.tsx`, `app/**/loading.tsx`, and `app/**/error.tsx` from coverage.
