# Claude Code Governance Templates

Ready-to-use governance templates for Claude Code, organized by tech stack.
Copy the folder matching your stack, adapt it to your project, and Claude Code applies your rules automatically on every session.
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f14ee7c0-07ca-42a9-9e08-6c011242dfa8" />

---

## Why this exists

Without structure, Claude Code generates inconsistent code, ignores your conventions, and repeats the same mistakes across sessions. This project fixes that with a hierarchy of `CLAUDE.md` files that load automatically — no prompting required.

If this saves you time, consider giving it a ⭐ — it helps others find the project.

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
| React / TypeScript only | [`react-only/`](./react-only/) | ✅ Ready |
| Angular only | [`angular-only/`](./angular-only/) | ✅ Ready |
| Vue.js only | [`vue-only/`](./vue-only/) | ✅ Ready |
| Next.js (full-stack) | [`nextjs/`](./nextjs/) | ✅ Ready |
| Node.js (Express) + React | `node-express-react/` | 🔜 Coming |
| Node.js (Express) + Angular | `node-express-angular/` | 🔜 Coming |
| Node.js (NestJS) + React | `nestjs-react/` | 🔜 Coming |
| Node.js (NestJS) + Angular | `nestjs-angular/` | 🔜 Coming |

### Python
| Stack | Folder | Status |
|---|---|---|
| Python (FastAPI) + React | [`python-fastapi-react/`](./python-fastapi-react/) | ✅ Ready |
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

### PHP
| Stack | Folder | Status |
|---|---|---|
| Laravel + React | `laravel-react/` | 🔜 Coming |
| Laravel + Vue.js | `laravel-vue/` | 🔜 Coming |
| Laravel + Angular | `laravel-angular/` | 🔜 Coming |
| Laravel API only | `laravel-only/` | 🔜 Coming |
| Symfony + React | `symfony-react/` | 🔜 Coming |
| Symfony API only | `symfony-only/` | 🔜 Coming |

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
| `TECH_LEAD` | 1 sentence max per concept, code only, no basic definitions, assumes senior reader |

---

## GovEval — Validate your governance config

Governance rules are only useful if Claude actually follows them.
**GovEval** is a test framework that validates AI behavior against your `CLAUDE.md` configuration.

```
Scenario prompt (natural developer request)
      ↓
Generator : Claude CLI — loads your CLAUDE.md + .claude/rules/ automatically
      ↓
Judge     : Mistral Large (independent model family — no shared bias)
            evaluates only the rule under test, scores 0–100
      ↓
PASS if score ≥ 80
```

It tests the 4 promises of the governance system:

| Category | What it validates |
|----------|-------------------|
| `architecture` | Layer separation, public_id in URLs, DTO separation |
| `security` | No IDOR, no raw SQL, no hardcoded secrets |
| `cost_control` | Minimal diffs, model suggestions, no boilerplate |
| `developer_level` | Response style adapted to JUNIOR vs TECH_LEAD |

### Choosing a judge model

The judge must come from a **different model family** than the generator to avoid bias.
Claude generates — the judge must not be Claude.

| Option | Model | Setup | Best for |
|--------|-------|-------|----------|
| **Mistral Large** (recommended) | `mistral-large-latest` | `MISTRAL_API_KEY` env var | Accuracy, strict scoring |
| **Local (Ollama)** | `qwen2.5:14b` or similar | `ollama pull qwen2.5:14b` | No API cost, offline |

To switch judge, change `JUDGE_MODEL` in `runner.py` and update the client accordingly.

### Run

**Via slash command (recommended):**

```bash
/gov-eval                          # all scenarios
/gov-eval --category security      # one category
/gov-eval --scenario SEC-01        # one scenario
```

Requires `MISTRAL_API_KEY` to be set and dependencies installed (`pip install -r <stack>/tests/requirements.txt`).

**Directly:**

```bash
cd java-react/tests
pip install -r requirements.txt
export MISTRAL_API_KEY=sk-...
python runner.py                        # all scenarios
python runner.py --category security    # one category
python runner.py --scenario SEC-01      # one scenario
```

Currently implemented for `java-react/`. See [`java-react/tests/`](./java-react/tests/) for full details.

### GovEval v1 vs v2

**v1 (current)** — Compliance testing: validates that Claude follows a single rule in a single prompt.

**v2 (roadmap)** — Governance system testing: validates that Claude correctly navigates the rule hierarchy.

| Test type | Question | Status |
|-----------|----------|--------|
| Compliance | Does Claude follow rule X? | ✅ v1 |
| Rule hierarchy | When global says OOP and project says Functional, does project win? | 🔜 v2 |
| Scoped boundary | Does `frontend.md` apply to `src/components/` but NOT `src/services/`? | 🔜 v2 |
| Rule recall | At turn 15 of a long session, does Claude still apply `public_id UUID`? | 🔜 v2 |

> Following a rule ≠ managing a system of rules.
> v2 tests the second, which is the real challenge of Claude Code governance.

---

## Installation

**Via plugin marketplace (recommended):**

```bash
/plugin marketplace add datallmhub/claude-governance
/plugin install claude-governance
```

Then run `/setup` in any project to initialize the governance system interactively.

**Local / development:**

```bash
git clone https://github.com/datallmhub/claude-governance.git
claude --plugin-dir /path/to/claude-governance
```

Then run `/setup` to select your stack.

**Manual (no plugin):**

1. Copy the stack folder into your project root.
2. Update `CLAUDE.md` with your project name, description, and stack versions.
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` (do not commit).
4. Set your experience level in `dev-level.md`.
5. Open Claude Code — the governance system is active immediately.

---

## `/setup` — Interactive stack initialization

Once the plugin is installed, run `/setup` in any project:

1. Select your stack from the list
2. The governance files are copied into your project
3. A `.claude-governance` marker is written so the session hook knows which stack is active
4. On every subsequent session, active rules are injected automatically at startup

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

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide.

The fastest way to contribute is to pick an open [`new-stack`](https://github.com/datallmhub/claude-governance/labels/new-stack) issue and follow the template structure from [`java-react/`](./java-react/).
