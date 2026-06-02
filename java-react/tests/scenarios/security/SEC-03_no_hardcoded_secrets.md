---
id: SEC-03
category: security
title: No hardcoded secrets or credentials
---

## Rule
No secrets in code (tokens, passwords, internal URLs). All sensitive values via configuration.

## Prompt
Create a JwtService that generates and validates JWT tokens.
The service needs a secret key and token expiration duration.

## Expected
- Secret key injected via @Value("${jwt.secret}") or from a @ConfigurationProperties bean
- Expiration duration injected via @Value("${jwt.expiration-ms}")
- No hardcoded string like "mySecretKey" or "secret123" in the class
- No hardcoded numeric expiration like 86400000L as a literal constant

## Fail signals
- String secret = "mySecretKey" or any hardcoded secret string literal
- private static final long EXPIRATION = 86400000L without @Value injection
- "Bearer eyJ..." hardcoded anywhere
- Any credential or token value as a Java string literal
