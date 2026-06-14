# Claude Code Governance Templates

Ready-to-use governance templates for Claude Code, organized by tech stack.
Rules load automatically on every session: no prompting required.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f14ee7c0-07ca-42a9-9e08-6c011242dfa8" />

---

## Why this exists

Without structure, Claude Code generates inconsistent code, ignores your conventions, and repeats the same mistakes across sessions. This project fixes that with a hierarchy of `CLAUDE.md` files that load automatically: no prompting required.

If this saves you time, consider giving it a ⭐: it helps others find the project.

**What you get:**
- Consistent code that respects your architecture and naming conventions
- Security rules enforced by default (no IDOR, no raw SQL, no hardcoded secrets)
- Cost control: precise diffs instead of full rewrites, right model for the right task
- Behavior adapted to the developer's experience level (Junior → Tech Lead)

---

## Installation

**Via plugin marketplace (recommended):**

```bash
/plugin marketplace add datallmhub/claude-governance
/plugin install claude-governance
```

Then run `/setup` in any project: select your stack, governance files are copied automatically, and rules inject at every session start.

**Local / development:**

```bash
git clone https://github.com/datallmhub/claude-governance.git
claude --plugin-dir /path/to/claude-governance
```

**Manual (no plugin):**

1. Copy the stack folder into your project root
2. Update `CLAUDE.md` with your project name and stack versions
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` (do not commit)
4. Set your experience level in `dev-level.md`

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
| React / TypeScript only | [`react-only/`](./react-only/) | ✅ Ready |
| Angular only | [`angular-only/`](./angular-only/) | ✅ Ready |
| Vue.js only | [`vue-only/`](./vue-only/) | ✅ Ready |
| Next.js (full-stack) | [`nextjs/`](./nextjs/) | ✅ Ready |
| Node.js (Express) + React | `node-express-react/` | 🔜 Coming |
| Node.js (NestJS) + React | [`nestjs-react/`](./nestjs-react/) | ✅ Ready |

### Python
| Stack | Folder | Status |
|---|---|---|
| Python (FastAPI) + React | [`python-fastapi-react/`](./python-fastapi-react/) | ✅ Ready |
| Python (Django) + React | `python-django-react/` | 🔜 Coming |
| Python (FastAPI) API only | `python-fastapi-only/` | 🔜 Coming |

### .NET / Go / PHP
| Stack | Folder | Status |
|---|---|---|
| .NET (ASP.NET Core) + React | `dotnet-react/` | 🔜 Coming |
| Go (Gin / Echo) + React | `go-react/` | 🔜 Coming |
| Laravel + React | `laravel-react/` | 🔜 Coming |
| Symfony + React | `symfony-react/` | 🔜 Coming |

---

## What's inside each template

```
<stack>/
├── CLAUDE.md                    # Project context: always loaded
├── CLAUDE.local.md.example      # Personal overrides (copy locally, never commit)
├── .claude/
│   ├── settings.json            # SessionStart hook: injects rules at session start
│   ├── rules/
│   │   ├── backend.md           # Backend rules: scoped to backend files only
│   │   ├── frontend.md          # Frontend rules: scoped to frontend files only
│   │   ├── database.md          # DB / migration rules
│   │   ├── testing.md           # Testing standards
│   │   ├── security.md          # Security rules: loaded on every file
│   │   ├── governance.md        # Git, PR, versioning, release process
│   │   └── dev-level.md         # Behavior by experience level
│   └── architecture/
│       ├── overview.md          # System architecture + key decisions
│       ├── api.md               # REST API contract
│       └── data-model.md        # Database schema
└── samples/                     # Code examples applying all the rules
```

---

## Load order

```
~/.claude/CLAUDE.md       ← personal preferences (your machine)
./CLAUDE.md               ← project rules (committed, shared)
./CLAUDE.local.md         ← personal overrides (gitignored)
.claude/rules/*.md        ← scoped rules (loaded per file path)
```

---

## Security

`security.md` loads on every file automatically. It enforces:

- **No IDOR**: `public_id UUID` in all URLs, never internal sequential IDs
- **No hardcoded secrets**: all credentials via environment variables
- **Safe tokens**: JWT in memory, refresh token in `HttpOnly; Secure` cookie
- **Injection prevention**: parameterized queries, input validated at system boundary
- **CORS locked down**: explicit origin whitelist, never `allowedOrigins("*")`

---

## Developer Experience Levels

One setting in `dev-level.md`: Claude adapts its verbosity automatically.

| Level | Behavior |
|---|---|
| `JUNIOR` | Step-by-step, full context, pitfalls flagged |
| `SENIOR` | Solution-first, 3 sentences max per concept |
| `EXPERT` | Code only, no explanations unless asked |
| `TECH_LEAD` | 1 sentence max, no prose, no fundamentals |

---

## GovEval: Validate your governance

Rules are useful only if Claude actually follows them. GovEval tests this automatically.

```
Natural prompt → Claude (generator) → Mistral Large (judge) → PASS / FAIL
```

The judge comes from a different model family to avoid self-evaluation bias.

```bash
/gov-eval                          # all scenarios
/gov-eval --category security      # one category
/gov-eval --scenario SEC-01        # one scenario
```

Requires `MISTRAL_API_KEY`. See [`java-react/tests/`](./java-react/tests/) for full details.

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide.

Pick an open [`new-stack`](https://github.com/datallmhub/claude-governance/labels/new-stack) issue: each one is a self-contained task with clear acceptance criteria.
