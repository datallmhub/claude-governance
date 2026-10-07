---
paths:
  - backend/**/*.py
---

# Backend Rules — Python / FastAPI

## Routers

- Always use `APIRouter(prefix="/api/v1/resource", tags=["resource"])`.
- Always declare response models: `@router.get("/", response_model=list[ProductResponse])`.
- Always use `status_code` explicitly: `@router.post("/", status_code=201)`.
- Always inject dependencies with `Depends()` — never instantiate services directly.

```python
router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    body: CreateProductRequest,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user),
):
    return await service.create(body, current_user)
```

## Schemas (Pydantic v2)

- Always use separate schemas for Request and Response. Never reuse the same model.
- Always use `model_config = ConfigDict(from_attributes=True)` on response schemas.
- Always expose `uid: UUID` in responses — never `id: int`.
- Always use `model_validator` or `field_validator` for cross-field business validation.

```python
class ProductResponse(BaseModel):
    uid: UUID = Field(alias="public_id")
    name: str
    price: Decimal
    in_stock: bool

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
```

## Services

- Always declare services as classes with `__init__(self, db: AsyncSession)`.
- Always inject via `Depends()`: `def get_product_service(db: AsyncSession = Depends(get_db))`.
- Always raise `HTTPException` with typed status codes for business errors.
- Always use `async def` for all service methods.

## Dependencies

- Always inject the DB session via `Depends(get_db)`. Never create `AsyncSession` manually.
- Always inject the current user via `Depends(get_current_user)` on protected endpoints.
- Always use `Security(get_current_user, scopes=["admin"])` for role-based access.

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
```

## Error Handling

- Always use `HTTPException(status_code=..., detail=...)` for expected errors.
- Always register custom exception handlers in `main.py` for domain exceptions.
- Always return RFC 7807-style error bodies: `{ "code": "...", "message": "..." }`.
- Never expose stack traces or internal error details in responses.

## Security

- Always extract the current user from the JWT token via `Depends(get_current_user)`.
- Always use `passlib[bcrypt]` for password hashing. Never use `hashlib` for passwords.
- Always validate `sub`, `exp`, and `iss` claims when decoding JWT tokens.
- Always sanitize logs: never log passwords, tokens, or email addresses.

## Async & Performance

- Always use `async def` for route handlers, services, and repository methods.
- Always use `select()` with explicit columns for list queries — avoid loading full models.
- Always paginate with `limit` and `offset` when the result set can exceed 100 rows.
- Always set `pool_pre_ping=True` on the SQLAlchemy engine to handle stale connections.
