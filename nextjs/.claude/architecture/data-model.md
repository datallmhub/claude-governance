# Architecture — Data Model (Prisma)

## Schema Conventions

Every model follows this pattern:

```prisma
model Example {
  // Internal PK — never exposed in API
  id        Int      @id @default(autoincrement())
  // Public identifier — used in all URLs and responses
  publicId  String   @unique @default(uuid())
  // Audit fields
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([publicId])
}
```

---

## Core Models

```prisma
model User {
  id           Int       @id @default(autoincrement())
  publicId     String    @unique @default(uuid())
  email        String    @unique
  name         String?
  role         Role      @default(USER)
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt

  sessions     Session[]
  products     Product[]

  @@index([publicId])
  @@index([email])
}

model Product {
  id          Int       @id @default(autoincrement())
  publicId    String    @unique @default(uuid())
  name        String
  description String?   @db.Text
  price       Decimal   @db.Decimal(10, 2)
  stock       Int       @default(0)
  active      Boolean   @default(true)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  userId      Int
  user        User      @relation(fields: [userId], references: [id])

  @@index([publicId])
  @@index([userId])
}

enum Role {
  USER
  ADMIN
}
```

---

## Rules

- Always add `@@index([publicId])` on every model.
- Always use `@db.Text` for long text fields.
- Always use `@db.Decimal` for monetary values.
- Always use Prisma enums for fixed value sets.
- Always use `onDelete: Cascade` explicitly when child records should be deleted with the parent.

## Soft Delete

For models requiring soft delete, add:
```prisma
deletedAt DateTime?
@@index([deletedAt])
```
Always filter with `where: { deletedAt: null }` in all queries.
