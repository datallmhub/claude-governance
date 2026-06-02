# Architecture — REST API

## Global Conventions

- Base URL: `/api/v1`
- Format: JSON (`Content-Type: application/json`)
- Auth: `Authorization: Bearer <access_token>` on all endpoints except `/auth/**`
- Pagination: `page` (0-based), `size` (default 20, max 100)
- Auto-generated docs: `/docs` (Swagger UI), `/redoc`

## Identifiers in URLs

Always use `public_id` UUID — never internal integer IDs.

```
✓  GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000
✗  GET /api/v1/products/42
```

## HTTP Status Codes

| Code | Meaning                                     |
|------|---------------------------------------------|
| 200  | Success — read / update                     |
| 201  | Resource created                            |
| 204  | Success with no body (DELETE)               |
| 400  | Validation failed (Pydantic error detail)   |
| 401  | Unauthenticated                             |
| 403  | Unauthorized (insufficient role)            |
| 404  | Resource not found                          |
| 409  | Conflict (duplicate)                        |
| 422  | Unprocessable entity (FastAPI default)      |
| 500  | Internal error — always logged              |

## Error Response Format

```json
{
  "code": "PRODUCT_NOT_FOUND",
  "message": "Product not found",
  "details": {}
}
```

## Endpoints

### Authentication
| Method | Endpoint              | Auth |
|--------|-----------------------|------|
| POST   | `/auth/register`      | No   |
| POST   | `/auth/token`         | No   |
| POST   | `/auth/refresh`       | No   |
| POST   | `/auth/logout`        | Yes  |

### Products (example domain)
| Method | Endpoint                     | Description          |
|--------|------------------------------|----------------------|
| GET    | `/products`                  | Paginated list       |
| POST   | `/products`                  | Create               |
| GET    | `/products/{uid}`            | Detail               |
| PUT    | `/products/{uid}`            | Update               |
| DELETE | `/products/{uid}`            | Soft delete          |

### Filter Parameters
```
?page=0&size=20
?sort=created_at&order=desc
?search=keyword
```
