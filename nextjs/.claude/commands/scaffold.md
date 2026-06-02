Generate a complete CRUD feature for the domain: $ARGUMENTS

Follow all rules in .claude/rules/frontend.md, .claude/rules/backend.md, and .claude/rules/database.md.

## Database — update Prisma schema:

1. Add the new model to `prisma/schema.prisma`
   - Include `id Int @id @default(autoincrement())`
   - Include `publicId String @unique @default(uuid())`
   - Include `createdAt DateTime @default(now())` and `updatedAt DateTime @updatedAt`
   - Add `@@index([publicId])`
2. Run `npx prisma migrate dev --name create_[name]` to generate the migration
3. Run `npx prisma generate` to regenerate the client

## Backend — generate these files:

4. `src/actions/[name].actions.ts`
   - 'use server' Server Actions: create, update, delete
   - Zod validation at top, auth() check, revalidatePath() after mutation
   - Return `{ data: T } | { error: string }`

5. `src/schemas/[name].schema.ts`
   - Zod schemas for create and update operations

## Frontend — generate these files:

6. `src/types/[name].ts`
   - TypeScript interface with `uid: string` (mapped from publicId)

7. `src/components/[Name]Card.tsx`
   - 'use client' only if it needs interactivity
   - shadcn/ui components only

8. `src/app/(dashboard)/[plural]/page.tsx`
   - Server Component by default
   - Fetch data directly with Prisma (no API route)

9. `src/app/(dashboard)/[plural]/[uid]/page.tsx`
   - Server Component, fetch by publicId
