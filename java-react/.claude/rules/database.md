---
paths:
  - backend/src/**/*Repository*.java
  - backend/src/**/*Entity*.java
  - infra/migrations/**/*.sql
---

# Database Rules — PostgreSQL / JPA / Flyway

## Flyway Migrations

- Always name files: `V{version}__{description_in_snake_case}.sql`. Ex: `V20250601_001__create_tasks_table.sql`.
- Always create a new Flyway script to modify the schema. Existing scripts are immutable.
- Always write idempotent DDL (`CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`).
- Always run the migration on a fresh DB before committing.
- Always include the rollback statement in a comment at the top of the script.

```sql
-- Rollback: DROP TABLE tasks;
CREATE TABLE IF NOT EXISTS tasks (
    id          BIGSERIAL    PRIMARY KEY,
    public_id   UUID         NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    title       VARCHAR(255) NOT NULL,
    status      VARCHAR(50)  NOT NULL DEFAULT 'todo',
    project_id  BIGINT       NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    org_id      BIGINT       NOT NULL REFERENCES organizations(id),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_public_id ON tasks(public_id);
CREATE INDEX IF NOT EXISTS idx_tasks_project   ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_org       ON tasks(org_id);
```

## Multi-Tenant

- Always add `org_id BIGINT NOT NULL REFERENCES organizations(id)` to every business table.
- Always put `org_id` first in composite indexes.
- Always filter on `org_id` in every JPQL and SQL query.
- Always extract `org_id` from the JWT token server-side; ignore any value sent in the request body.

## JPA Entities

- Always use `snake_case` for table names and column names.
- Always declare `@Column(name = "...")` explicitly; rely on Hibernate naming conventions only for tests.
- Always use `@SequenceGenerator` with `allocationSize = 50` for BigSerial primary keys.
- Always declare `@Version Long version` on entities subject to concurrent modifications.
- Always use explicit `CascadeType` values (`PERSIST`, `MERGE`); use `ALL` only when cascade delete is intentional.

```java
@Entity
@Table(name = "tasks")
public class TaskEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "task_seq")
    @SequenceGenerator(name = "task_seq", sequenceName = "tasks_id_seq", allocationSize = 50)
    private Long id;

    @Column(name = "public_id", nullable = false, updatable = false)
    private UUID publicId;

    @Column(name = "org_id", nullable = false)
    private Long orgId;

    @Version
    private Long version;
}
```

## Queries and Performance

- Always paginate with `Pageable` when the result set can exceed 100 rows.
- Always use `@EntityGraph` or JPQL fetch join to avoid N+1 queries.
- Always run `EXPLAIN ANALYZE` on any new query targeting a table with more than 10,000 rows.
- Always use Spring Data Projection interfaces or record DTOs for partial projections.

```java
public interface TaskSummary {
    String getPublicId();
    String getTitle();
    String getStatus();
}

Page<TaskSummary> findSummariesByOrgId(Long orgId, Pageable pageable);
```

## Transactions

- Always place `@Transactional` at the service layer, not the controller layer.
- Always annotate read-only methods with `@Transactional(readOnly = true)`.
- Always resolve external HTTP calls outside the transactional block. Keep transactions short.

## SQL Conventions

- Always write SQL keywords in UPPERCASE in Flyway scripts.
- Always write one constraint per line in `CREATE TABLE` statements.
- Always declare indexes separately after the `CREATE TABLE` statement, never inline.
- Always use `TIMESTAMPTZ` instead of `TIMESTAMP` for date/time columns.
