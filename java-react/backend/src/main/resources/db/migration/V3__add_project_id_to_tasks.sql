ALTER TABLE tasks
    ADD COLUMN project_id BIGINT NOT NULL REFERENCES projects(id);

CREATE INDEX idx_tasks_project_id ON tasks (project_id);
