---
paths:
  - backend/src/**/*.spec.ts
  - backend/test/**/*.ts
  - frontend/src/**/*.test.ts
  - frontend/src/**/*.test.tsx
  - frontend/src/**/*.spec.ts
---

# Testing Rules

## General Principles

- Always test one behavior per test. A failing test must pinpoint exactly what broke.
- Always name tests to describe the expected behavior, not the method name.
- Always make tests independent of execution order.

## Backend — Unit Tests (Jest)

- Always test services in isolation. Mock `@InjectRepository` with `getRepositoryToken()`.
- Always name tests: `should {behavior} when {condition}`.
- Always cover: success, resource not found, invalid input, access denied.
- Never boot the full application for unit tests.

```typescript
describe('TasksService', () => {
  let service: TasksService;
  const mockRepo = { findOne: jest.fn(), save: jest.fn() };

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        TasksService,
        { provide: getRepositoryToken(TaskEntity), useValue: mockRepo },
      ],
    }).compile();
    service = module.get(TasksService);
  });

  it('should throw TaskNotFoundException when task does not exist', async () => {
    mockRepo.findOne.mockResolvedValue(null);
    await expect(service.findByPublicId('uuid', 1)).rejects.toThrow(TaskNotFoundException);
  });
});
```

## Backend — Controller Tests (Supertest)

- Always use `@nestjs/testing` to create a testing module with mocked services.
- Always use Supertest for HTTP assertions on controllers.
- Always verify status codes, response shape, and guard behavior.

```typescript
describe('TasksController (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      controllers: [TasksController],
      providers: [{ provide: TasksService, useValue: mockTasksService }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    app = module.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();
  });

  it('POST /api/v1/tasks returns 201', () => {
    return request(app.getHttpServer())
      .post('/api/v1/tasks')
      .send({ title: 'Fix bug', projectPublicId: validUuid })
      .expect(201)
      .expect(res => expect(res.body.uid).toBeDefined());
  });
});
```

## Backend — Integration Tests (Testcontainers)

- Always use Testcontainers PostgreSQL for repository integration tests.
- Always suffix integration test files with `.integration-spec.ts`.
- Always run migrations before tests and clean up between test suites.
- Always verify organization isolation: data from org A must not be readable by org B.

```typescript
describe('TaskRepository (integration)', () => {
  let container: StartedTestContainer;
  let dataSource: DataSource;

  beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:16').start();
    dataSource = await createTestDataSource(container.getConnectionUri());
    await dataSource.runMigrations();
  });
});
```

## Backend — Coverage

- Target minimum 80% coverage on `services/` and custom repositories.
- Always run `npm run test:cov` before opening a PR.

## Frontend — Unit Tests (Vitest / Testing Library)

- Always test visible behavior, not implementation details.
- Always select elements by accessible role or visible text.
- Always use MSW to intercept API calls; never mock `fetch` directly.
- Always render components with required providers via a shared `renderWithProviders` helper.

```typescript
it('shows error state when fetch fails', async () => {
  server.use(http.get('/api/v1/tasks', () => HttpResponse.error()));
  renderWithProviders(<TaskListPage />);
  expect(await screen.findByRole('alert')).toBeInTheDocument();
});
```

## Frontend — Hook Tests

- Always test hooks with `renderHook` from Testing Library.
- Always use MSW to simulate server responses.

## Frontend — Coverage

- Target minimum 70% coverage on `/components` and `/hooks`.
- Always exclude Vite config files, pure type files, and index barrels from coverage.
