---
paths:
  - src/**/*.spec.ts
  - e2e/**/*.ts
---

# Testing Rules — Angular / Jest / Cypress

## General Principles

- Always test one behavior per test.
- Always name tests to describe expected behavior: `should display error when service fails`.
- Always make tests independent of execution order.

## Unit Tests (Jest + Angular Testing Library)

- Always use `TestBed.configureTestingModule` with only the strictly required providers.
- Always mock services with `jest.fn()` or a manual stub — never the real HTTP service.
- Always test the component's rendered output, not its internal properties.

```typescript
it('should display product name', () => {
  const { getByText } = render(ProductCardComponent, {
    componentProperties: { product: mockProduct }
  });
  expect(getByText(mockProduct.name)).toBeTruthy();
});
```

## Service Tests

- Always test services in isolation with mocked `HttpClient` using `HttpClientTestingModule`.
- Always verify `HttpTestingController` expectations after each test.

## E2E Tests (Cypress / Playwright)

- Always seed test data via API calls in `beforeEach`, not via UI interactions.
- Always use `data-cy` attributes for E2E selectors — keep them separate from CSS/test selectors.
- Always run E2E tests against a real dev server, never mocked.

## Coverage

- Target minimum 75% on services and components.
- Always exclude auto-generated files (`*.module.ts`, `environment.ts`) from coverage.
