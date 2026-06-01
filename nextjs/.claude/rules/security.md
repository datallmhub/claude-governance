---
paths:
  - src/**/*.tsx
  - src/**/*.ts
  - src/app/api/**/*
  - src/actions/**/*
---

# Security Rules — Next.js

## Authentication

- Always use `auth()` from NextAuth to get the session in Server Components and Server Actions.
- Always protect Server Actions by calling `auth()` at the top and throwing if unauthenticated.
- Always store session tokens in `HttpOnly; Secure; SameSite=Strict` cookies — NextAuth handles this by default.
- Always configure `trustHost: true` only in trusted reverse-proxy environments.

```typescript
export async function deleteProduct(uid: string) {
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');
  // ...
}
```

## IDOR Prevention

- Always use `public_id UUID` in URLs and API responses — never expose Prisma's internal `id`.
- Always verify resource ownership in Server Actions: check that the record belongs to the authenticated user.

## Input Validation

- Always validate Server Action and API route inputs with Zod before any DB operation.
- Always return structured errors from Server Actions — never expose raw Prisma errors.

```typescript
const schema = z.object({ title: z.string().min(1), price: z.number().positive() });
const parsed = schema.safeParse(input);
if (!parsed.success) return { error: parsed.error.flatten() };
```

## Secrets & Environment Variables

- Always access secrets via `process.env` on the server only — never in Client Components.
- Always prefix public variables with `NEXT_PUBLIC_` only when they are truly safe to expose.
- Always add `.env*.local` to `.gitignore`. Never commit secrets.

## Security Headers

- Always configure security headers in `next.config.ts`:

```typescript
const securityHeaders = [
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
];
```

## CSRF

- Always use Server Actions for mutations — Next.js provides built-in CSRF protection for Server Actions.
- Never use API routes for state-mutating operations that could be triggered cross-origin.

## Dependency Security

- Always run `npm audit` before merging to main.
- Always pin dependency versions — no open ranges in production.
