---
paths:
  - src/lib/db.ts
  - prisma/**/*
---

# Database Rules — Prisma / PostgreSQL

## Schema

- Always add `publicId String @unique @default(uuid())` to every model exposed via API.
- Always use `id Int @id @default(autoincrement())` as internal PK — never expose it.
- Always add `createdAt DateTime @default(now())` and `updatedAt DateTime @updatedAt` on every model.
- Always use `@@index` for columns used in frequent `where` clauses.

```prisma
model Product {
  id          Int      @id @default(autoincrement())
  publicId    String   @unique @default(uuid())
  name        String
  price       Decimal  @db.Decimal(10, 2)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([publicId])
}
```

## Migrations

- Always run `npx prisma migrate dev --name description` to create migrations.
- Always review the generated SQL before applying (`prisma/migrations/`).
- Never edit an existing migration file. Create a new one.
- Always run `npx prisma generate` after schema changes.

## Queries

- Always select only needed fields with `select` or `include` — avoid fetching full models for lists.
- Always use `prisma.$transaction()` for operations that must succeed or fail together.
- Always paginate list queries with `skip` and `take`.
- Always filter with `where: { publicId: uid }` in API-facing queries — never `where: { id }`.

```typescript
// Correct — paginated, typed selection
const products = await prisma.product.findMany({
  where: { active: true },
  select: { publicId: true, name: true, price: true },
  orderBy: { createdAt: 'desc' },
  skip: page * size,
  take: size,
});
```

## Conventions

- Always use `camelCase` for Prisma field names; Prisma maps to `snake_case` in PostgreSQL automatically.
- Always add `@db.Text` for long text fields, `@db.Decimal` for prices.
- Always use enums for fixed value sets: `enum Status { ACTIVE ARCHIVED }`.
