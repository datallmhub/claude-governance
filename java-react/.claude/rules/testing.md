---
paths:
  - backend/src/test/**/*.java
  - frontend/src/**/*.test.ts
  - frontend/src/**/*.test.tsx
  - frontend/src/**/*.spec.ts
---

# Testing Rules

## General Principles

- Always test one behavior per test. A failing test must pinpoint exactly what broke.
- Always name tests to describe the expected behavior, not the method name.
- Always write one assertion per conditional path; extract a separate test for each branch.
- Always make tests independent of execution order.

## Backend — Unit Tests (JUnit 5 / Mockito)

- Always test services in isolation with Mockito. Mock repositories, not the class under test.
- Always name tests: `should{Behavior}When{Condition}`.
- Always cover: success, resource not found, invalid input, access denied.
- Always instantiate the class under test directly; only mock its dependencies.
- Always use `@WebMvcTest` + MockMvc for controller tests, not `@SpringBootTest`.

```java
@Test
void shouldThrowNotFoundWhenTaskDoesNotExist() {
    when(taskRepository.findByPublicId(any())).thenReturn(Optional.empty());
    assertThrows(TaskNotFoundException.class, () -> taskService.findByPublicId(UUID.randomUUID()));
}
```

```java
@WebMvcTest(TaskController.class)
class TaskControllerTest {
    @Autowired MockMvc mvc;
    @MockBean TaskService taskService;

    @Test
    void shouldReturn201WhenTaskCreated() throws Exception {
        when(taskService.create(any())).thenReturn(sampleTaskResponse());
        mvc.perform(post("/api/v1/tasks").contentType(APPLICATION_JSON).content(validJson()))
           .andExpect(status().isCreated())
           .andExpect(jsonPath("$.uid").exists());
    }
}
```

## Backend — Integration Tests (Testcontainers)

- Always use `@DataJpaTest` + Testcontainers PostgreSQL for repository tests.
- Always use Testcontainers for integration tests. H2 has SQL behavior differences with PostgreSQL.
- Always suffix integration test classes with `IT`: `TaskRepositoryIT`.
- Always start each test from a clean state: `@Transactional` + rollback, or `@Sql` cleanup.

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@Testcontainers
class TaskRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", postgres::getJdbcUrl);
    }
}
```

## Backend — Coverage

- Target minimum 80% coverage on `service` and `repository` packages.
- Always exclude `@Configuration` classes from coverage reporting.
- Always generate the JaCoCo report before opening a PR: `mvn jacoco:report`.

## Frontend — Unit Tests (Vitest / Testing Library)

- Always test visible behavior, not implementation details.
- Always select elements by accessible role or visible text.
- Always use MSW (Mock Service Worker) to intercept API calls; never mock `fetch` directly.
- Always render components with the required providers using a shared `renderWithProviders` helper.

```typescript
// test-utils.tsx
export function renderWithProviders(ui: ReactElement) {
  return render(ui, { wrapper: AppProviders });
}

// Correct element selection
const button = screen.getByRole('button', { name: /create task/i });
```

## Frontend — Hook Tests

- Always test hooks with `renderHook` from Testing Library.
- Always use MSW to simulate server responses in hooks that fetch data.

```typescript
it('should return tasks when fetch succeeds', async () => {
  server.use(http.get('/api/v1/tasks', () => HttpResponse.json([sampleTask()])));
  const { result } = renderHook(() => useTaskList('some-uid'), { wrapper: QueryWrapper });
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data).toHaveLength(1);
});
```

## Frontend — Coverage

- Target minimum 70% coverage on `/components` and `/hooks`.
- Always exclude Vite config files, pure type files and index barrels from coverage.
