---
paths:
  - "**/*"
---

# Governance Rules

## Git Workflow

- Always work on a feature branch. Never commit directly to `main`.
- Always name branches: `feature/short-description`, `fix/short-description`, `chore/short-description`.
- Always keep branches short-lived. Open a PR within 2 days of starting a branch.
- Always rebase on `main` before opening a PR. Never merge `main` into a feature branch.

## Commit Messages (Conventional Commits)

Always follow the format: `type(scope): short description`

| Type       | When to use                                      |
|------------|--------------------------------------------------|
| `feat`     | New feature                                      |
| `fix`      | Bug fix                                          |
| `refactor` | Code change without feature or fix               |
| `test`     | Adding or updating tests                         |
| `chore`    | Build, tooling, dependencies                     |
| `docs`     | Documentation only                               |
| `perf`     | Performance improvement                          |
| `security` | Security fix or hardening                        |

```
feat(task): add assignee filtering to task list endpoint
fix(auth): refresh token cookie not set on subdomain
security(jwt): enforce audience claim validation
```

- Always write the description in lowercase imperative form: "add", "fix", "update" — not "added", "fixes", "updating".
- Always keep the subject line under 72 characters.
- Always add a body when the commit introduces a non-obvious decision or workaround.

## Pull Requests

- Always open a PR before merging, even for solo work.
- Always fill in the PR template: summary, test plan, breaking changes.
- Always link the PR to its issue or ticket.
- Always require at least one approval before merging to `main`.
- Always ensure all CI checks pass before merging (build, tests, lint, security scan).
- Always squash commits when merging unless individual commits tell a meaningful story.
- Never merge a PR with failing tests or unresolved blocking review comments.

## Code Review Standards

- Always review for correctness first, then clarity, then style.
- Always provide a specific suggestion when requesting a change — not just flagging a problem.
- Always distinguish between blocking issues and suggestions:
  - Blocking: `[blocking] This query is missing org_id filter — IDOR risk.`
  - Suggestion: `[nit] Could simplify with optional chaining here.`
- Always approve explicitly. Do not merge without explicit approval.

## API Versioning

- Always version the API with a URL prefix: `/api/v1/`, `/api/v2/`.
- Always maintain the previous major version for a minimum of 3 months after a new version is released.
- Always document breaking changes in `CHANGELOG.md` before merging.
- Always treat these changes as breaking: removing a field, changing a field type, changing HTTP status codes, removing an endpoint.

## Breaking Changes

- Always open an RFC (comment in the issue or a dedicated PR discussion) before implementing a breaking change.
- Always bump the API major version for any breaking change to a public endpoint.
- Always notify consumers at least 2 sprints before a breaking change goes live.

## Dependency Management

- Always pin versions in `package.json` and commit `package-lock.json`.
- Always review the changelog and license before adding a new dependency.
- Always run `npm audit` before each release.
- Always update dependencies in a dedicated `chore(deps):` PR, not mixed with feature work.

## Documentation

- Always update `CLAUDE.md` when the architecture, stack, or critical constraints change.
- Always update `.claude/architecture/api.md` when adding, modifying, or deprecating an endpoint.
- Always update `.claude/architecture/data-model.md` when the schema changes.
- Always update `.claude/rules/` when a new coding convention is established or an old one is retired.
- Always document architectural decisions in `.claude/architecture/overview.md` with the decision, reason, and impact.

## Release Process

1. All tests pass on `main` (unit + integration + security scan).
2. `CHANGELOG.md` is updated with the new version and release notes.
3. Version is bumped in root and workspace `package.json` files.
4. A Git tag is created: `v{major}.{minor}.{patch}`.
5. The tag triggers the CI/CD pipeline for production deployment.

Always use semantic versioning: `MAJOR.MINOR.PATCH`.

## Environment Parity

- Always keep dev, staging, and production environments structurally identical (same Docker images, same config structure).
- Always test on staging with production-like data volumes before releasing to production.
- Always use feature flags for gradual rollouts of significant changes.
