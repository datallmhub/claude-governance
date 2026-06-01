# Architecture — Server Actions & API Routes

## Server Actions (primary mutation mechanism)

Server Actions are the default for all state-changing operations.

### Naming convention
- File: `src/actions/[domain].actions.ts`
- Function: `createProduct`, `updateOrder`, `deleteUser`

### Return type contract

```typescript
type ActionResult<T> =
  | { data: T; error?: never }
  | { error: string | FieldErrors; data?: never };
```

### Standard pattern

```typescript
'use server';
export async function createProduct(input: unknown): Promise<ActionResult<ProductResponse>> {
  const session = await auth();
  if (!session) return { error: 'Unauthorized' };

  const parsed = createProductSchema.safeParse(input);
  if (!parsed.success) return { error: parsed.error.flatten().fieldErrors };

  const product = await prisma.product.create({
    data: { ...parsed.data, publicId: crypto.randomUUID() }
  });
  revalidatePath('/products');
  return { data: toProductResponse(product) };
}
```

---

## API Routes (secondary — external integrations only)

| Route | Purpose |
|---|---|
| `POST /api/webhooks/stripe` | Stripe payment events |
| `GET /api/auth/[...nextauth]` | NextAuth OAuth callbacks |

### API Route pattern

```typescript
export async function POST(request: Request) {
  const body = await request.json();
  const parsed = webhookSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: 'Invalid payload' }, { status: 400 });
  // process...
  return NextResponse.json({ received: true });
}
```

---

## Identifiers in URLs

Always use `publicId` (UUID) in URLs — never Prisma's internal `id`.

```
✓  /products/550e8400-e29b-41d4-a716-446655440000
✗  /products/42
```

---

## Caching Strategy

| Data type | Strategy |
|---|---|
| Static content | `fetch` with `cache: 'force-cache'` |
| Frequently updated data | `fetch` with `revalidate: 60` (seconds) |
| User-specific data | `no-store` or `unstable_cache` with user tag |
| After mutation | `revalidatePath()` or `revalidateTag()` |
