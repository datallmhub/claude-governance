Review the current file or selection for security issues.

Follow .claude/rules/security.md as the checklist.

Check for:

**IDOR / ID Exposure**
- Internal integer IDs exposed in URLs or response bodies
- @PathVariable Long id instead of UUID
- id field present in response DTOs

**Injection**
- String concatenation in JPQL or SQL queries
- User input used in dynamic queries without parameterization

**Authentication & Authorization**
- Endpoints missing @PreAuthorize
- organizationId read from request body instead of JWT token
- JWT claims not fully validated (exp, iss, aud)

**Secrets**
- Hardcoded credentials, tokens, or API keys
- Secrets in application.properties instead of environment variables

**Logging**
- PII logged (email, name, token, password)
- Stack traces returned to the client

**Frontend**
- JWT stored in localStorage or sessionStorage
- dangerouslySetInnerHTML used without sanitization
- any type used instead of unknown + type guard

Report findings as:
- [CRITICAL] — must fix before merge
- [HIGH] — should fix before merge
- [MEDIUM] — fix in follow-up
- [INFO] — good practice suggestion
