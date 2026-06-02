-- Rollback: ALTER TABLE tasks DROP COLUMN IF EXISTS due_date;

ALTER TABLE tasks
    ADD COLUMN due_date DATE NULL;
