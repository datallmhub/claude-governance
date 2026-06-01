---
paths:
  - backend/src/**/*.java
  - frontend/src/**/*.ts
  - frontend/src/**/*.tsx
  - infra/**/*
---

# Security Rules

## Secrets Management

- Always store secrets in environment variables or a secrets manager. Never hardcode them in source code.
- Always add `.env*` files to `.gitignore`. Never commit them.
- Always use `@Value("${property}")` or Spring Config Server to inject secrets in Spring Boot.
- Always rotate secrets after any accidental exposure — treat a committed secret as compromised immediately.

## Authentication & Tokens

- Always store JWT access tokens in memory (JS variable), never in `localStorage` or `sessionStorage`.
- Always store the refresh token in an `HttpOnly; Secure; SameSite=Strict` cookie — never accessible from JavaScript.
- Always validate the JWT signature, expiry (`exp`), issuer (`iss`) and audience (`aud`) on every request.
- Always use a minimum key size of 256 bits for HMAC-SHA256 JWT signing.
- Always implement token refresh before expiry. Access token TTL: 15 min. Refresh token TTL: 7 days.

```java
// JWT filter: validate all claims
Claims claims = Jwts.parserBuilder()
    .setSigningKey(signingKey)
    .requireIssuer("taskflow-api")
    .requireAudience("taskflow-web")
    .build()
    .parseClaimsJws(token)
    .getBody();
```

## Authorization

- Always use `@PreAuthorize` at the method level for fine-grained access control. Never rely on URL-only security.
- Always verify that the resource being accessed belongs to the authenticated user's organization before returning it.
- Always apply the principle of least privilege: grant only the minimum permissions required.
- Always deny by default — public endpoints are the exception and must be explicitly declared.

```java
// Always verify org ownership, not just authentication
@PreAuthorize("hasRole('USER')")
public TaskResponse getTask(UUID taskUid, Long orgId) {
    return taskRepository.findByPublicIdAndOrgId(taskUid, orgId)
        .map(mapper::toResponse)
        .orElseThrow(() -> new TaskNotFoundException(taskUid));
}
```

## Input Validation & Injection Prevention

- Always validate all user input at the system boundary using Bean Validation (`@Valid`) or Zod.
- Always use parameterized queries (JPQL named parameters or `@Query` with `:param`). Never concatenate user input into SQL strings.
- Always sanitize HTML content before rendering it with `dangerouslySetInnerHTML`. Prefer avoiding it entirely.
- Always validate file uploads: allowed MIME types, maximum size, filename sanitization.

```java
// Correct: parameterized JPQL
@Query("SELECT t FROM TaskEntity t WHERE t.title LIKE %:search% AND t.orgId = :orgId")
List<TaskEntity> searchByTitle(@Param("search") String search, @Param("orgId") Long orgId);

// Forbidden: string concatenation
// "SELECT * FROM tasks WHERE title LIKE '%" + userInput + "%'"
```

## Output Encoding & XSS Prevention

- Always use React's JSX rendering (not `dangerouslySetInnerHTML`) — JSX escapes output by default.
- Always use `text` responses, not `html` responses, in Spring REST controllers.
- Always set `Content-Type: application/json` explicitly on API responses.
- Always configure security headers via Spring Security:

```java
http.headers(headers -> headers
    .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
    .frameOptions(frame -> frame.deny())
    .xssProtection(xss -> xss.enable())
    .referrerPolicy(referrer -> referrer.policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN))
);
```

## CORS

- Always whitelist specific origins. Never use `allowedOrigins("*")` in production.
- Always restrict allowed methods to only those actually used (GET, POST, PUT, PATCH, DELETE).
- Always set `allowCredentials(true)` only when cookies are required, and only with explicit origins.

```java
@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://taskflow.app"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE"));
    config.setAllowCredentials(true);
    return new UrlBasedCorsConfigurationSource();
}
```

## CSRF

- Always enable CSRF protection for endpoints accessed by browsers (cookie-based sessions).
- JWT-only stateless APIs may disable CSRF only if no cookies are used for authentication.
- Always use `SameSite=Strict` on the refresh token cookie as a defense-in-depth measure.

## Logging & Error Exposure

- Always log security events: failed login attempts, token rejections, authorization failures.
- Always exclude PII from logs: emails, names, phone numbers, addresses, tokens, passwords.
- Always return generic error messages to the client for authentication and authorization failures.

```java
// Correct: generic message to client, details in server log
log.warn("Authentication failed for user: {} — {}", maskedEmail, reason);
throw new BadCredentialsException("Invalid credentials");

// Forbidden: exposing internals
throw new BadCredentialsException("User john@example.com not found in database");
```

## Dependency Security

- Always run `mvn dependency-check:check` (OWASP) before releasing.
- Always run `npm audit` and resolve critical vulnerabilities before merging to main.
- Always pin dependency versions in `pom.xml` and `package.json`. Avoid open ranges (`^`, `~`) in production.
- Always review and understand each new dependency before adding it.

## Cryptography

- Always use BCrypt (strength ≥ 12) for password hashing. Never use MD5, SHA-1 or plain SHA-256.
- Always use `java.security.SecureRandom` for token generation. Never use `Math.random()`.
- Always use standard library cryptographic functions. Never implement custom encryption.

## HTTPS & Transport Security

- Always enforce HTTPS in production. Redirect HTTP to HTTPS at the infrastructure level.
- Always set `Strict-Transport-Security: max-age=31536000; includeSubDomains` in production.
- Always use TLS 1.2 minimum. Disable TLS 1.0 and 1.1.
