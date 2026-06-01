---
paths:
  - src/app/api/**/*.ts
  - src/actions/**/*.ts
  - src/lib/**/*.ts
---

# Backend Rules — Next.js Server Actions & API Routes

## Server Actions

- Always validate inputs with Zod at the top of every Server Action.
- Always call `auth()` first in protected actions — throw if no session.
- Always return a typed result: `{ data: T } | { error: string }`.
- Always call `revalidatePath()` or `revalidateTag()` after successful mutations.
- Always keep Server Actions in `/actions`, one file per domain (`product.actions.ts`).

```typescript
'use server';
export async function createProduct(input: unknown): Promise<ActionResult<Product>> {
  const session = await auth();
  if (!session) return { error: 'Unauthorized' };

  const parsed = createProductSchema.safeParse(input);
  if (!parsed.success) return { error: parsed.error.flatten().fieldErrors };

  const product = await prisma.product.create({ data: { ...parsed.data, publicId: crypto.randomUUID() } });
  revalidatePath('/products');
  return { data: toProductResponse(product) };
}
```

## API Routes

- Always use API routes only for webhooks, OAuth callbacks, or third-party integrations.
- Always validate request body with Zod before processing.
- Always return `NextResponse.json()` with explicit HTTP status codes.
- Always protect API routes with `auth()` — return 401 for unauthenticated requests.

## Database (Prisma)

- Always use the Prisma singleton from `lib/db.ts` — never instantiate `PrismaClient` directly.
- Always use `prisma.$transaction()` for multi-table writes.
- Always select only needed fields — avoid `findUnique` with no `select` on large models.
- Always expose `publicId` (UUID) in responses — never expose Prisma's internal `id`.

```typescript
// lib/db.ts — singleton
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
export const prisma = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

## Caching

- Always use `unstable_cache` for expensive server-side data fetching.
- Always tag cached data with `revalidateTag` for targeted invalidation.
- Always set explicit `revalidate` values on `fetch` calls — never rely on default behavior.
