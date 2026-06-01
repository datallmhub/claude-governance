---
paths:
  - src/**/*.ts
  - src/**/*.html
---

# Frontend Rules — Angular / TypeScript

## TypeScript

- Always use `unknown` + type guard instead of `any`.
- Always keep `strict: true` and `strictTemplates: true` in `tsconfig.json`.
- Always type `HttpClient` calls explicitly: `http.get<Product[]>(url)`.

## Components

- Always use standalone components (`standalone: true`). No `NgModule` declarations.
- Always set `changeDetection: ChangeDetectionStrategy.OnPush` on every component.
- Always use the `inject()` function for dependency injection — not constructor injection.
- Always use the `async` pipe or `toSignal()` in templates — never subscribe manually without cleanup.

```typescript
@Component({
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<div *ngIf="products$ | async as products">...</div>`
})
export class ProductListComponent {
  private productService = inject(ProductService);
  products$ = this.productService.getAll();
}
```

## Services

- Always provide services in `root` via `providedIn: 'root'`.
- Always return `Observable<T>` from service methods — never subscribe inside a service.
- Always use `takeUntilDestroyed()` for subscriptions in components.

## Routing

- Always lazy-load feature routes: `loadComponent: () => import(...)`.
- Always protect routes with `canActivate` guards.
- Always use `Router.navigate()` with typed route arrays, never string concatenation.

## Forms

- Always use Reactive Forms for any form with validation.
- Always declare `FormGroup` with typed controls: `new FormControl<string>('')`.
- Always display validation errors using a shared `ControlErrorComponent`.

## State Management

- Use Angular Signals for local and shared component state.
- Use NgRx Store only for complex, cross-feature global state.
- Always derive computed values with `computed()` — never duplicate state.

## Error Handling

- Always handle HTTP errors in a global `HttpInterceptor`.
- Always show user-facing error messages via a `SnackBarService`, not `alert()`.
- Always log errors to the console only in development (`!environment.production`).

## Performance

- Always lazy-load feature modules and routes.
- Always use `trackBy` in `*ngFor` directives.
- Always use `@defer` blocks for below-the-fold heavy components (Angular 17+).
