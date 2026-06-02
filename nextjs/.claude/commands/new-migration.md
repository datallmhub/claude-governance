Generate a new Prisma migration for: $ARGUMENTS

Follow all rules in .claude/rules/database.md.

1. Update `prisma/schema.prisma` with the required changes.
2. Run `npx prisma migrate dev --name [description_in_snake_case]`.
3. Verify the generated SQL in `prisma/migrations/` includes:
   - `publicId` with UUID type and unique constraint
   - Appropriate indexes
   - No breaking changes to existing columns without a deprecation plan
4. Run `npx prisma generate` after the migration.
5. Never edit an existing migration file — create a new one.
