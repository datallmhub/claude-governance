---
paths:
  - src/**/*.test.ts
  - src/**/*.spec.ts
  - tests/**/*.ts
---

# Testing Rules — Vue 3 / Vitest / Playwright

## General Principles

- Always test one behavior per test.
- Always name tests to describe expected behavior.
- Always make tests independent of execution order.

## Component Tests (Vitest + Vue Testing Library)

- Always mount components with `render()` from `@testing-library/vue`.
- Always provide required plugins (Pinia, Router) via the `global` option.
- Always select elements by accessible role or visible text — never by CSS selector.
- Always use MSW to intercept API calls in composable tests.

```typescript
it('should show product name', () => {
  const { getByText } = render(ProductCard, {
    props: { product: mockProduct },
    global: { plugins: [createTestingPinia()] }
  });
  expect(getByText(mockProduct.name)).toBeTruthy();
});
```

## Composable Tests

- Always test composables with `mount` + a wrapper component, or directly with Vitest if they have no DOM dependency.
- Always use MSW for composables that call the API.

## E2E Tests (Playwright)

- Always seed data via API in `beforeEach`, not via UI navigation.
- Always use `page.getByRole()` or `page.getByText()` — never CSS selectors in E2E.
- Always run Playwright against the dev server (`npm run dev`).

## Coverage

- Target minimum 70% on `/components` and `/composables`.
- Always run `npm run test -- --coverage` before opening a PR.
