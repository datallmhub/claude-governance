# Architecture — Data Model

## Entity-Relationship Diagram (simplified)

```
organizations
    │
    ├──< users (via organization_members)
    │
    ├──< projects
    │       │
    │       ├──< project_members (users assigned to the project)
    │       │
    │       └──< tasks
    │               │
    │               ├──< comments
    │               ├──< task_attachments
    │               └── assignee (user)
    │
    └──< notifications
```

---

## Main Tables

### `organizations`
| Column      | Type         | Constraints             | Description              |
|-------------|--------------|-------------------------|--------------------------|
| id          | BIGSERIAL    | PK                      |                          |
| name        | VARCHAR(100) | NOT NULL                |                          |
| slug        | VARCHAR(50)  | NOT NULL, UNIQUE        | URL identifier           |
| plan        | VARCHAR(20)  | NOT NULL DEFAULT 'free' | free / pro / enterprise  |
| created_at  | TIMESTAMPTZ  | NOT NULL DEFAULT NOW    |                          |

### `users`
| Column        | Type         | Constraints                                  | Description     |
|---------------|--------------|----------------------------------------------|-----------------|
| id            | BIGSERIAL    | PK                                           | Internal only   |
| public_id     | UUID         | NOT NULL, UNIQUE, DEFAULT gen_random_uuid()  | API identifier  |
| email         | VARCHAR(255) | NOT NULL, UNIQUE                             |                 |
| password_hash | VARCHAR(255) | NOT NULL                                     | BCrypt          |
| display_name  | VARCHAR(100) | NOT NULL                                     |                 |
| avatar_url    | VARCHAR(500) |                                              |                 |
| created_at    | TIMESTAMPTZ  | NOT NULL                                     |                 |
| last_login_at | TIMESTAMPTZ  |                                              |                 |

### `organization_members`
| Column    | Type        | Constraints                        |
|-----------|-------------|------------------------------------|
| org_id    | BIGINT      | FK → organizations(id), NOT NULL   |
| user_id   | BIGINT      | FK → users(id), NOT NULL           |
| role      | VARCHAR(20) | NOT NULL — OWNER / ADMIN / MEMBER  |
| joined_at | TIMESTAMPTZ | NOT NULL                           |
| PK        |             | (org_id, user_id)                  |

### `projects`
| Column      | Type         | Constraints                                  | Description              |
|-------------|--------------|----------------------------------------------|--------------------------|
| id          | BIGSERIAL    | PK                                           | Internal only            |
| public_id   | UUID         | NOT NULL, UNIQUE, DEFAULT gen_random_uuid()  | API identifier           |
| org_id      | BIGINT       | FK → organizations, NOT NULL                 | Multi-tenant isolation   |
| name        | VARCHAR(255) | NOT NULL                                     |                          |
| description | TEXT         |                                              |                          |
| status      | VARCHAR(20)  | NOT NULL DEFAULT 'active'                    | active / archived        |
| owner_id    | BIGINT       | FK → users                                   |                          |
| created_at  | TIMESTAMPTZ  | NOT NULL                                     |                          |
| updated_at  | TIMESTAMPTZ  | NOT NULL                                     |                          |

### `tasks`
| Column      | Type         | Constraints                                  | Description              |
|-------------|--------------|----------------------------------------------|--------------------------|
| id          | BIGSERIAL    | PK                                           | Internal only            |
| public_id   | UUID         | NOT NULL, UNIQUE, DEFAULT gen_random_uuid()  | API identifier           |
| org_id      | BIGINT       | FK → organizations, NOT NULL                 | Multi-tenant isolation   |
| project_id  | BIGINT       | FK → projects, NOT NULL                      |                          |
| title       | VARCHAR(255) | NOT NULL                                     |                          |
| description | TEXT         |                                              |                          |
| status      | VARCHAR(20)  | NOT NULL DEFAULT 'todo'                      | todo/in_progress/done    |
| priority    | VARCHAR(10)  | NOT NULL DEFAULT 'medium'                    | low/medium/high/critical |
| assignee_id | BIGINT       | FK → users                                   |                          |
| due_date    | DATE         |                                              |                          |
| created_by  | BIGINT       | FK → users, NOT NULL                         |                          |
| created_at  | TIMESTAMPTZ  | NOT NULL                                     |                          |
| updated_at  | TIMESTAMPTZ  | NOT NULL                                     |                          |
| deleted_at  | TIMESTAMPTZ  |                                              | Soft delete              |
| version     | BIGINT       | NOT NULL DEFAULT 0                           | Optimistic locking       |

### `comments`
| Column     | Type        | Constraints              |
|------------|-------------|--------------------------|
| id         | BIGSERIAL   | PK                       |
| task_id    | BIGINT      | FK → tasks, NOT NULL     |
| org_id     | BIGINT      | FK → organizations, NN   |
| author_id  | BIGINT      | FK → users, NOT NULL     |
| content    | TEXT        | NOT NULL                 |
| created_at | TIMESTAMPTZ | NOT NULL                 |
| edited_at  | TIMESTAMPTZ |                          |

### `refresh_tokens`
| Column     | Type         | Constraints       |
|------------|--------------|-------------------|
| id         | BIGSERIAL    | PK                |
| user_id    | BIGINT       | FK → users, NN    |
| token_hash | VARCHAR(255) | NOT NULL, UNIQUE  |
| expires_at | TIMESTAMPTZ  | NOT NULL          |
| revoked_at | TIMESTAMPTZ  |                   |
| created_at | TIMESTAMPTZ  | NOT NULL          |

---

## Indexes

```sql
-- UUID resolution (all API requests go through here)
CREATE UNIQUE INDEX idx_users_public_id    ON users(public_id);
CREATE UNIQUE INDEX idx_projects_public_id ON projects(public_id);
CREATE UNIQUE INDEX idx_tasks_public_id    ON tasks(public_id);

-- Performance: org-scoped search (all multi-tenant entities)
CREATE INDEX idx_projects_org    ON projects(org_id);
CREATE INDEX idx_tasks_org       ON tasks(org_id);
CREATE INDEX idx_tasks_project   ON tasks(project_id, org_id);
CREATE INDEX idx_tasks_assignee  ON tasks(assignee_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_comments_task   ON comments(task_id);

-- Authentication
CREATE INDEX idx_users_email         ON users(email);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id) WHERE revoked_at IS NULL;
```

---

## Soft Delete Rules

- Tables `projects` and `tasks` implement soft delete via `deleted_at`.
- All queries must include `WHERE deleted_at IS NULL` except audit reports.
- In JPA, use `@Where(clause = "deleted_at IS NULL")` on affected entities.
- Physical DELETE is never used on these tables from the application.

---

## Allowed Enum Values

| Field                  | Allowed values                             |
|------------------------|--------------------------------------------|
| `tasks.status`         | `todo`, `in_progress`, `review`, `done`    |
| `tasks.priority`       | `low`, `medium`, `high`, `critical`        |
| `projects.status`      | `active`, `archived`                       |
| `org_members.role`     | `OWNER`, `ADMIN`, `MEMBER`                 |
| `organizations.plan`   | `free`, `pro`, `enterprise`                |
