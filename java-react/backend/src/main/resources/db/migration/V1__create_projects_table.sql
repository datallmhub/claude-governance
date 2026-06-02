CREATE TABLE projects (
    id              BIGSERIAL       PRIMARY KEY,
    public_id       UUID            NOT NULL UNIQUE,
    organization_id BIGINT          NOT NULL,
    name            VARCHAR(255)    NOT NULL,
    description     VARCHAR(2000),
    created_at      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_projects_organization_id ON projects (organization_id);
CREATE INDEX idx_projects_public_id ON projects (public_id);
