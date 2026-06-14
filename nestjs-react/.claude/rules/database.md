---
paths:
  - backend/src/**/*.entity.ts
  - backend/src/**/entities/**/*.ts
  - backend/src/migrations/**/*.ts
  - backend/prisma/**/*
---

# Database Rules — PostgreSQL / TypeORM / Prisma

## TypeORM Migrations

- Always name files: `{timestamp}-{DescriptionInPascalCase}.ts`. Ex: `1718361600000-CreateTasksTable.ts`.
- Always create a new migration to modify the schema. Existing migrations are immutable.
- Always set `synchronize: false` in all environments except throwaway local scratch DBs.
- Always run `npm run migration:run` on a fresh DB before committing.
- Always implement both `up()` and `down()` methods.

```typescript
export class CreateTasksTable1718361600000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      CREATE TABLE IF NOT EXISTS tasks (
        id          SERIAL PRIMARY KEY,
        public_id   UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
        title       VARCHAR(255) NOT NULL,
        org_id      INTEGER NOT NULL REFERENCES organizations(id),
        project_id  INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_tasks_public_id ON tasks(public_id);
      CREATE INDEX IF NOT EXISTS idx_tasks_org ON tasks(org_id);
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP TABLE IF EXISTS tasks`);
  }
}
```

## TypeORM Entities

- Always use `@Entity('snake_case_table')` with explicit `@Column({ name: 'snake_case' })`.
- Always add `publicId: string` with `@Column({ type: 'uuid', unique: true, default: () => 'gen_random_uuid()' })`.
- Always add `organizationId` to every business entity in multi-tenant apps.
- Always use `@CreateDateColumn()` and `@UpdateDateColumn()` for audit fields.
- Always use `eager: false` on relations — load explicitly with `relations` or QueryBuilder joins.

```typescript
@Entity('tasks')
export class TaskEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ name: 'public_id', type: 'uuid', unique: true, default: () => 'gen_random_uuid()' })
  publicId: string;

  @Column({ name: 'org_id' })
  organizationId: number;

  @Column({ length: 255 })
  title: string;

  @CreateDateColumn({ name: 'created_at', type: 'timestamptz' })
  createdAt: Date;
}
```

## Prisma (alternative ORM)

- If using Prisma: always add `publicId String @unique @default(uuid()) @db.Uuid` to every exposed model.
- Always run `npx prisma migrate dev --name description` for schema changes. Never edit applied migrations.
- Always use the generated `PrismaClient` via a NestJS `PrismaService` wrapper — never instantiate `PrismaClient` in feature code.

```prisma
model Task {
  id             Int      @id @default(autoincrement())
  publicId       String   @unique @default(uuid()) @map("public_id") @db.Uuid
  organizationId Int      @map("org_id")
  title          String   @db.VarChar(255)
  createdAt      DateTime @default(now()) @map("created_at") @db.Timestamptz

  @@index([organizationId])
  @@map("tasks")
}
```

## Multi-Tenant

- Always add `org_id INTEGER NOT NULL REFERENCES organizations(id)` to every business table.
- Always put `org_id` first in composite indexes.
- Always filter on `organizationId` in every query — TypeORM `where`, QueryBuilder, or Prisma `where`.
- Always extract `organizationId` from JWT server-side; ignore any value sent in the request body.

## Queries and Performance

- Always paginate with `skip`/`take` or `nestjs-typeorm-paginate` when results can exceed 100 rows.
- Always use QueryBuilder join aliases to avoid N+1 queries on list endpoints.
- Always create indexes on `public_id`, `org_id`, and foreign key columns used in WHERE clauses.
- Always use `TIMESTAMPTZ` instead of `TIMESTAMP` for date/time columns.

## Transactions

- Always use `@Transactional()` (typeorm-transactional) or `queryRunner.startTransaction()` for multi-table writes.
- Always keep transactions in the service layer, not controllers.
- Always resolve external HTTP calls outside transactional blocks.

## SQL Conventions

- Always write SQL keywords in UPPERCASE in raw migration queries.
- Always declare indexes separately after `CREATE TABLE`, not inline.
- Always use parameterized queries via TypeORM/Prisma APIs. Never string-concatenate user input.
