---
paths:
  - backend/**/*.py
  - frontend/src/**/*.ts
  - frontend/src/**/*.tsx
---

# Security Rules — FastAPI + React

## Secrets Management

- Always store secrets in environment variables loaded via `pydantic-settings`.
- Always use a `.env` file locally — add it to `.gitignore`. Never commit it.
- Never hardcode API keys, database URLs, or JWT secrets in source code.

```python
class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")
```

## Authentication & JWT

- Always use `OAuth2PasswordBearer` for JWT token extraction in FastAPI.
- Always validate `sub`, `exp`, `iss` claims when decoding tokens.
- Always use a minimum secret length of 32 characters for HMAC-SHA256 signing.
- Always store JWT access tokens in memory (JS variable) — never in `localStorage`.
- Always store refresh tokens in `HttpOnly; Secure; SameSite=Strict` cookies.
- Always set short TTLs: access token 15 min, refresh token 7 days.

```python
def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
```

## IDOR Prevention

- Always use `public_id UUID` in all API paths and response bodies.
- Always verify that the resource belongs to the authenticated user before returning it.
- Never expose the internal integer `id` in any response or URL.

## Input Validation

- Always use Pydantic schemas to validate all request bodies — FastAPI enforces this automatically.
- Always add field constraints in Pydantic: `Field(min_length=1, max_length=255)`.
- Always use parameterized SQLAlchemy queries — never string-format user input into SQL.

## CORS

- Always whitelist specific origins in `CORSMiddleware`. Never use `allow_origins=["*"]` in production.
- Always restrict allowed methods to those actually used.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Logging

- Always log security events: failed logins, invalid tokens, authorization failures.
- Always exclude PII from logs: emails, names, tokens, passwords.
- Always return generic error messages to clients for auth failures.

```python
# Correct
logger.warning("Authentication failed", extra={"reason": "invalid_token"})
raise HTTPException(status_code=401, detail="Invalid credentials")

# Forbidden
raise HTTPException(status_code=401, detail=f"User {email} not found")
```

## Dependencies

- Always run `pip-audit` before every release to check for known vulnerabilities.
- Always pin all dependencies in `requirements.txt` or `pyproject.toml`.
- Always use `bcrypt` via `passlib[bcrypt]` for password hashing — never `hashlib`.

## Security Headers

- Always add security headers via a middleware or `starlette` response headers:
  - `X-Frame-Options: DENY`
  - `X-Content-Type-Options: nosniff`
  - `Strict-Transport-Security: max-age=31536000`
