# Claude Code Governance Templates

Ready-to-use governance templates for Claude Code, organized by tech stack.
Copy the folder matching your stack, adapt it to your project, and Claude Code applies your rules automatically on every session.

---

## Why this exists

Without structure, Claude Code generates inconsistent code, ignores your conventions, and repeats the same mistakes across sessions. This project fixes that with a hierarchy of `CLAUDE.md` files that load automatically — no prompting required.

**What you get:**
- Consistent code that respects your architecture and naming conventions
- Security rules enforced by default (no IDOR, no raw SQL, no hardcoded secrets)
- Cost control — precise diffs instead of full rewrites, right model for the right task
- Behavior adapted to the developer's experience level (Junior → Tech Lead)

---

## Available stacks

### Java
| Stack | Folder | Status |
|---|---|---|
| Java (Spring Boot) + React (TypeScript) | [`java-react/`](./java-react/) | ✅ Ready |
| Java (Spring Boot) + Angular | `java-angular/` | 🔜 Coming |
| Java (Spring Boot) + Vue.js | `java-vue/` | 🔜 Coming |
| Java (Spring Boot) API only | `java-only/` | 🔜 Coming |

### JavaScript / TypeScript
| Stack | Folder | Status |
|---|---|---|
| React / TypeScript only | `react-only/` | 🔜 Coming |
| Angular only | `angular-only/` | 🔜 Coming |
| Vue.js only | `vue-only/` | 🔜 Coming |
| Next.js (full-stack) | `nextjs/` | 🔜 Coming |
| Node.js (NestJS) + React | `nestjs-react/` | 🔜 Coming |
| Node.js (NestJS) + Angular | `nestjs-angular/` | 🔜 Coming |

### Python
| Stack | Folder | Status |
|---|---|---|
| Python (FastAPI) + React | `python-fastapi-react/` | 🔜 Coming |
| Python (FastAPI) + Angular | `python-fastapi-angular/` | 🔜 Coming |
| Python (Django) + React | `python-django-react/` | 🔜 Coming |
| Python (FastAPI) API only | `python-fastapi-only/` | 🔜 Coming |

### .NET
| Stack | Folder | Status |
|---|---|---|
| .NET (ASP.NET Core) + React | `dotnet-react/` | 🔜 Coming |
| .NET (ASP.NET Core) + Angular | `dotnet-angular/` | 🔜 Coming |
| .NET (ASP.NET Core) API only | `dotnet-only/` | 🔜 Coming |

### Go
| Stack | Folder | Status |
|---|---|---|
| Go (Gin / Echo) + React | `go-react/` | 🔜 Coming |
| Go API only | `go-only/` | 🔜 Coming |

---

## What's inside each template

```
<stack>/
├── CLAUDE.md                    # Project context — always loaded
├── CLAUDE.local.md.example      # Personal overrides (copy locally, never commit)
├── .claude/
│   ├── rules/
│   │   ├── backend.md           # Backend rules — loaded for backend files only
│   │   ├── frontend.md          # Frontend rules — loaded for frontend files only
│   │   ├── database.md          # DB / migration rules
│   │   ├── testing.md           # Testing standards
│   │   ├── security.md          # Security rules (OWASP, JWT, secrets, injection)
│   │   ├── governance.md        # Git, PR, versioning, release process
│   │   └── dev-level.md         # Behavior by experience level
│   └── architecture/
│       ├── overview.md          # System architecture + key decisions
│       ├── api.md               # REST API contract
│       └── data-model.md        # Database schema
└── samples/                     # Code examples applying all the rules
```

---

## Security

The `security.md` rule file loads automatically on every backend, frontend, and infra file. It enforces:

- **No IDOR** — internal sequential IDs never exposed in URLs. Every resource uses a `public_id UUID`.
- **No hardcoded secrets** — all credentials via environment variables, never in source code.
- **Safe tokens** — JWT in memory only, refresh token in `HttpOnly; Secure` cookie.
- **Injection prevention** — parameterized queries only, input validated at system boundary.
- **CORS locked down** — explicit origin whitelist, never `allowedOrigins("*")` in production.
- **Dependency scanning** — OWASP check + `npm audit` before every release.

---

## Cost Control (FinOps)

Claude Code costs are driven by output tokens and context window size. The governance system reduces both.

| Rule | Impact |
|---|---|
| Scoped rules load only when needed | Smaller context per session |
| Precise diffs instead of full file rewrites | Fewer output tokens |
| Right model for the right task | Haiku for tests/docs, Sonnet for features, Opus for architecture |
| 200-line limit per rule file | Context stays lean |
| Stop and ask after 2 failed retries | No wasted loops |

> Suggest `claude-haiku-4-5` for writing tests, docs, or fixing simple syntax errors.
> Escalate to a stronger model only when stuck on complex architectural problems.

---

## Developer Experience Levels

Set the active level in `.claude/rules/dev-level.md` (one line to change):

```
**Current level: SENIOR**
```

Override personally in `CLAUDE.local.md` (not committed):
```
Active level: JUNIOR
```

| Level | Claude's behavior |
|---|---|
| `JUNIOR` | Full explanations, step-by-step, common pitfalls flagged, code with full context |
| `SENIOR` | Concise, solution-first, 3 sentences max per concept |
| `EXPERT` | No explanations unless asked, minimal code snippets, precise vocabulary |
| `TECH_LEAD` | Architecture framing, team impact, doc update requirements, RFC triggers |

---

## How to use

1. Copy the stack folder into your project root.
2. Update `CLAUDE.md` with your project name, description, and stack versions.
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` (do not commit).
4. Set your experience level in `dev-level.md`.
5. Open Claude Code — the governance system is active immediately.

---

## Load order

```
~/.claude/CLAUDE.md       ← personal preferences (your machine)
./CLAUDE.md               ← project rules (committed, shared)
./CLAUDE.local.md         ← personal overrides (gitignored)
.claude/rules/*.md        ← scoped rules (loaded per file path)
```

---

## Contributing

PRs welcome — new stack templates especially.
Each template must include all 7 rule files and follow the same folder structure.
