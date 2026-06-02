Generate a new Flyway migration script for: $ARGUMENTS

Follow all rules in .claude/rules/database.md.

1. Determine the next version number by reading existing files in `infra/migrations/`.
2. Create `infra/migrations/V[YYYYMMDD]_[NNN]__[description_in_snake_case].sql`
3. The script must include:
   - A rollback comment at the top: `-- Rollback: ...`
   - `CREATE TABLE IF NOT EXISTS` or `ALTER TABLE` as appropriate
   - A `public_id UUID NOT NULL UNIQUE DEFAULT gen_random_uuid()` column if creating a new table
   - Separate `CREATE INDEX IF NOT EXISTS` statements after the table definition
   - All columns with explicit NOT NULL constraints and defaults
   - `TIMESTAMPTZ` for all date/time columns
4. Never modify an existing migration file.
