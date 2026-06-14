---
paths:
  - backend/src/**/*.ts
  - frontend/src/**/*.ts
  - frontend/src/**/*.tsx
  - infra/**/*
---

# Security Rules

## Secrets Management

- Always store secrets in environment variables loaded via `@nestjs/config` `ConfigModule`.
- Always add `.env*` files to `.gitignore`. Never commit them.
- Always inject secrets through `ConfigService.getOrThrow()`. Never hardcode in source code.
- Always rotate secrets after any accidental exposure — treat a committed secret as compromised immediately.

```typescript
// config/jwt.config.ts
export default registerAs('jwt', () => ({
  secret: process.env.JWT_SECRET, // validated once at bootstrap via Joi
  expiresIn: '15m',
}));
```

## Authentication & Tokens

- Always store JWT access tokens in memory (JS variable), never in `localStorage` or `sessionStorage`.
- Always store the refresh token in an `HttpOnly; Secure; SameSite=Strict` cookie — never accessible from JavaScript.
- Always validate JWT signature, expiry (`exp`), issuer (`iss`), and audience (`aud`) in `JwtStrategy.validate()`.
- Always use a minimum key size of 256 bits for HMAC-SHA256 JWT signing.
- Always implement token refresh before expiry. Access token TTL: 15 min. Refresh token TTL: 7 days.

```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(config: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: config.getOrThrow('JWT_SECRET'),
      issuer: 'taskflow-api',
      audience: 'taskflow-web',
    });
  }
}
```

## Authorization

- Always use `@UseGuards(JwtAuthGuard, RolesGuard)` for protected routes. Never rely on URL patterns alone.
- Always verify that the resource belongs to the authenticated user's organization before returning it.
- Always apply least privilege: grant only the minimum permissions required.
- Always deny by default — public endpoints must be explicitly marked with `@Public()` decorator.

```typescript
@Get(':taskUid')
@UseGuards(JwtAuthGuard)
async getTask(
  @Param('taskUid', ParseUUIDPipe) taskUid: string,
  @CurrentUser() user: AuthUser,
) {
  return this.tasksService.findByPublicId(taskUid, user.organizationId);
}
```

## Input Validation & Injection Prevention

- Always validate all user input at the system boundary via global `ValidationPipe` + `class-validator`.
- Always use TypeORM QueryBuilder or Prisma parameterized queries. Never concatenate user input into SQL strings.
- Always sanitize HTML before rendering with `dangerouslySetInnerHTML`. Prefer avoiding it entirely.
- Always validate file uploads: allowed MIME types, maximum size, filename sanitization.

```typescript
// Correct: parameterized QueryBuilder
this.taskRepo.createQueryBuilder('t')
  .where('t.title ILIKE :search', { search: `%${search}%` })
  .andWhere('t.organizationId = :orgId', { orgId })
  .getMany();

// Forbidden: string concatenation
// `SELECT * FROM tasks WHERE title LIKE '%${userInput}%'`
```

## Output Encoding & XSS Prevention

- Always use React JSX rendering (not `dangerouslySetInnerHTML`) — JSX escapes output by default.
- Always return JSON from NestJS controllers — never HTML responses from API endpoints.
- Always set security headers via `helmet` middleware in `main.ts`:

```typescript
app.use(helmet());
app.enableCors({
  origin: config.get<string>('CORS_ORIGIN'),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
});
```

## CORS

- Always whitelist specific origins via `ConfigService`. Never use `origin: '*'` in production.
- Always restrict allowed methods to only those actually used.
- Always set `credentials: true` only when cookies are required, and only with explicit origins.

## CSRF

- Always enable CSRF protection for cookie-based auth endpoints accessed by browsers.
- JWT-only stateless APIs may skip CSRF only if no cookies are used for authentication.
- Always use `SameSite=Strict` on the refresh token cookie as defense-in-depth.

## Logging & Error Exposure

- Always log security events: failed login attempts, token rejections, authorization failures via NestJS `Logger`.
- Always exclude PII from logs: emails, names, phone numbers, tokens, passwords.
- Always return generic error messages to the client for authentication and authorization failures.

```typescript
// Correct
this.logger.warn(`Authentication failed — reason: ${reason}`);
throw new UnauthorizedException('Invalid credentials');

// Forbidden
throw new UnauthorizedException('User john@example.com not found');
```

## Dependency Security

- Always run `npm audit` and resolve critical vulnerabilities before merging to main.
- Always pin dependency versions in `package.json`. Avoid open ranges in production lockfiles.
- Always review new dependencies before adding them.

## Cryptography

- Always use `bcrypt` (cost factor ≥ 12) via `@nestjs/passport` compatible hash service. Never MD5, SHA-1, or plain SHA-256 for passwords.
- Always use `crypto.randomBytes()` for token generation. Never `Math.random()`.
- Always use standard library cryptographic functions. Never implement custom encryption.

## HTTPS & Transport Security

- Always enforce HTTPS in production. Redirect HTTP to HTTPS at the infrastructure level.
- Always set `Strict-Transport-Security` via Helmet in production.
- Always use TLS 1.2 minimum.
