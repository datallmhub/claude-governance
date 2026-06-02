Generate a new Alembic migration for: $ARGUMENTS

Follow all rules in .claude/rules/database.md.

1. Run `alembic revision --autogenerate -m "[description]"` to generate the migration file.
2. Review the generated file in `backend/alembic/versions/`.
3. Verify it includes:
   - `public_id` column with `UUID` type and `server_default=sa.text("gen_random_uuid()")`
   - Separate index creation with `op.create_index()`
   - `TIMESTAMP(timezone=True)` for all date/time columns
   - A working `downgrade()` that reverses the `upgrade()`
4. Never edit an existing migration file — create a new one instead.
