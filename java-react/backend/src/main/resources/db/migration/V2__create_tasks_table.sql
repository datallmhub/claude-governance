CREATE TABLE tasks (
    id              BIGSERIAL       PRIMARY KEY,
    public_id       UUID            NOT NULL UNIQUE,
    organization_id BIGINT          NOT NULL,
    title           VARCHAR(255)    NOT NULL,
    status          VARCHAR(50)     NOT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_organization_id ON tasks (organization_id);
CREATE INDEX idx_tasks_public_id ON tasks (public_id);
