---
paths:
  - src/**/*.test.ts
  - src/**/*.test.tsx
  - src/**/*.spec.ts
---

# Testing Rules — React / Vitest / Testing Library

## General Principles

- Always test one behavior per test. A failing test must pinpoint exactly what broke.
- Always name tests to describe expected behavior: `should show error when fetch fails`.
- Always make tests independent of execution order.
- Always write one assertion per conditional path.

## Components

- Always test visible behavior, not implementation details.
- Always select elements by accessible role or visible text — never by CSS selector or `data-testid` unless last resort.
- Always render components with required providers using a shared `renderWithProviders` helper.
- Always use MSW (Mock Service Worker) to intercept API calls — never mock `fetch` directly.

```tsx
// test-utils.tsx
export function renderWithProviders(ui: ReactElement) {
  return render(ui, { wrapper: AppProviders });
}

const button = screen.getByRole('button', { name: /add to cart/i });
```

## Hooks

- Always test custom hooks with `renderHook` from Testing Library.
- Always use MSW to simulate server responses in hooks that fetch data.

## Coverage

- Target minimum 70% on `/components` and `/hooks`.
- Always exclude config files, pure type files, and index barrels from coverage.
- Always run `npm run test -- --coverage` before opening a PR.
