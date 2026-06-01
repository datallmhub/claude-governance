-- Rollback: DROP TABLE products;
CREATE TABLE IF NOT EXISTS products (
    id          BIGSERIAL    PRIMARY KEY,
    public_id   UUID         NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    price       NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    stock       INT          NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category    VARCHAR(100) NOT NULL,
    image_url   VARCHAR(500),
    active      BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_public_id ON products(public_id);
CREATE INDEX IF NOT EXISTS idx_products_category  ON products(category) WHERE active = TRUE;
