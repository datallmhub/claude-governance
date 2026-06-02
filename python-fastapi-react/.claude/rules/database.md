---
paths:
  - backend/app/models/**/*.py
  - backend/app/repositories/**/*.py
  - backend/alembic/**/*
---

# Database Rules — SQLAlchemy 2.0 / Alembic / PostgreSQL

## Alembic Migrations

- Always generate migrations with `alembic revision --autogenerate -m "description"`.
- Always review the generated script before applying — autogenerate misses check constraints and custom indexes.
- Always create a new migration file to modify the schema. Never edit an existing migration.
- Always include a `downgrade()` function that reverses the `upgrade()`.
- Always name migrations descriptively: `2026_06_01_001_create_products_table`.

```python
def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("public_id", postgresql.UUID(as_uuid=True), nullable=False,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_products_public_id", "products", ["public_id"], unique=True)

def downgrade() -> None:
    op.drop_table("products")
```

## SQLAlchemy Models

- Always use `mapped_column()` and `Mapped[]` type annotations (SQLAlchemy 2.0 style).
- Always add `public_id: Mapped[UUID]` with `default=uuid4, unique=True` to every exposed model.
- Always add `created_at` and `updated_at` audit columns to every model.
- Always declare relationships with `lazy="select"` — never `lazy="joined"` unless profiled.

```python
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
```

## Queries (SQLAlchemy 2.0 style)

- Always use `select()` statements — never the legacy `session.query()` API.
- Always use `await session.execute(select(...))` with `scalars()` or `mappings()`.
- Always paginate list queries with `.limit(size).offset(page * size)`.
- Always filter on `public_id` in API-facing queries — never on `id`.

```python
async def find_by_public_id(self, public_id: UUID) -> Product | None:
    result = await self.db.execute(
        select(Product).where(Product.public_id == public_id, Product.active == True)
    )
    return result.scalar_one_or_none()

async def find_all(self, page: int, size: int) -> list[Product]:
    result = await self.db.execute(
        select(Product).where(Product.active == True)
        .order_by(Product.created_at.desc())
        .limit(size).offset(page * size)
    )
    return list(result.scalars().all())
```

## Transactions

- Always use `async with session.begin()` for multi-table writes.
- Always commit explicitly — never rely on autocommit.
- Always rollback on exception — the `get_db` dependency handles this via `try/finally`.

## Conventions

- Always use `snake_case` for table names and column names.
- Always use `TIMESTAMP(timezone=True)` for date/time columns — never `TIMESTAMP` without timezone.
- Always use `Numeric(10, 2)` for monetary values — never `Float`.
- Always create indexes for columns used in frequent `WHERE` clauses.
