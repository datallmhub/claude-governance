# Architecture — Data Model

## SQLAlchemy Model Conventions

Every model follows this pattern:

```python
class Example(Base):
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4, unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), onupdate=func.now())
```

## Core Tables

### `users`
| Column        | Type                  | Constraints       |
|---------------|-----------------------|-------------------|
| id            | SERIAL                | PK — internal     |
| public_id     | UUID                  | UNIQUE — API use  |
| email         | VARCHAR(255)          | UNIQUE, NOT NULL  |
| password_hash | VARCHAR(255)          | NOT NULL          |
| is_active     | BOOLEAN               | DEFAULT TRUE      |
| created_at    | TIMESTAMPTZ           | NOT NULL          |
| updated_at    | TIMESTAMPTZ           |                   |

### `refresh_tokens`
| Column     | Type        | Constraints      |
|------------|-------------|------------------|
| id         | SERIAL      | PK               |
| user_id    | INTEGER     | FK → users       |
| token_hash | VARCHAR(255)| UNIQUE, NOT NULL |
| expires_at | TIMESTAMPTZ | NOT NULL         |
| revoked_at | TIMESTAMPTZ |                  |

## Indexes

```sql
CREATE UNIQUE INDEX idx_users_public_id    ON users(public_id);
CREATE UNIQUE INDEX idx_users_email        ON users(email);
CREATE INDEX        idx_refresh_token_hash ON refresh_tokens(token_hash);
```

## Soft Delete

For models requiring soft delete, add:
```python
deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
```
Always filter with `.where(Model.deleted_at.is_(None))` in all active-record queries.

## Allowed Enum Values

Define Python enums and map to PostgreSQL:
```python
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
```
