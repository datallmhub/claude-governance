# Claude Code Governance Templates

Ready-to-use governance templates for Claude Code, organized by tech stack.
Rules load automatically on every session: no prompting required.

If this saves you time, consider giving it a ⭐: it helps others find the project.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f14ee7c0-07ca-42a9-9e08-6c011242dfa8" />

---

## Why this exists

Without structure, Claude Code generates inconsistent code, ignores your conventions, and repeats the same mistakes across sessions. This project fixes that with a hierarchy of `CLAUDE.md` files that load automatically: no prompting required.

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
├── govbuild.json                # Which rules are generated, and with which stack wording
├── .claude/
│   ├── settings.json            # SessionStart hook: injects rules at session start
│   ├── rules/
│   │   ├── backend.md           # Backend rules: scoped to backend files only
│   │   ├── frontend.md          # Frontend rules: scoped to frontend files only
│   │   ├── database.md          # DB / migration rules
│   │   ├── testing.md           # Testing standards
│   │   ├── security.md          # Generated from policies/security/
│   │   ├── architecture.md      # Generated from policies/architecture/
│   │   ├── governance.md        # Generated from core/rules/
│   │   └── dev-level.md         # Generated from core/rules/
│   └── architecture/
│       ├── overview.md          # System architecture + key decisions
│       ├── api.md               # REST API contract
│       └── data-model.md        # Database schema
├── .github/instructions/        # Same policies, rendered for GitHub Copilot
└── samples/                     # Code examples applying all the rules
```

Generated files carry a header saying so. Edit the source — `policies/` or `core/rules/` — and run
`tools/govctl build`. `tools/govctl check` fails CI when a generated file was edited by hand.

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

## Policies and enforcement

A rule that only lives in Markdown is advice. In `policies/` it is a record with an id, a severity,
the surfaces it is enforced on, the requirements, the per-stack bindings, and — when a deterministic
check exists — the patterns that detect a violation:

```yaml
id: SEC-006
title: CORS configuration
severity: high
enforcement:
  agent: true
  ci: true
  pre_commit: true
requirements:
  - Always whitelist explicit origins. Never use a wildcard origin in production.
detect:
  - id: SEC-006.wildcard-origin
    evaluator: regex
    include: ["**/*.java", "**/*.ts", "**/*.tsx", "**/*.py"]
```

One source, several outputs: the Claude Code rule file, the Copilot instruction file, and the check
that runs on the code the agent produced.

```bash
tools/governance check --changed    # BLOCK on critical / high, WARN below, exit code included
tools/governance report --format json
```

```
Governance Report

ARCH-001 Layered boundaries                         PASS
ARCH-002 Public identifiers                         FAIL  1 finding(s)
SEC-001  Secrets management                         PASS
SEC-003  Authorization and IDOR prevention          AGENT-ONLY

Decision: BLOCK
```

`AGENT-ONLY` means the policy is injected into the agent but has no automated check yet — the gap
between what is written and what is verified stays visible instead of being implied. A finding is
waived in place with `governance: allow <detector-id> — reason`, which keeps the exception auditable
instead of pushing a team to disable the check.

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

**GovEval is to governance rules what unit tests are to code.**

It does not test Claude in isolation. It tests Claude **as configured by this repo** — `CLAUDE.md` + `.claude/rules/` + dev-level + everything else loaded automatically.

The developer prompt never repeats the rules:

```
Developer request → Claude Code runtime (rules loaded silently) → Generated code → Judge → PASS / FAIL
```

**Example — `SEC-01`:**

| Step | Result |
|---|---|
| Prompt | "Create GET /tasks" |
| Generated | `organizationId` read from JWT, not the request |
| Judge | Mistral Large — isolation verified |
| Result | ✅ PASS — 100/100 |

The judge (Mistral Large) is a different model family than the generator (Claude), so it isn't grading its own work.

```bash
/gov-eval                          # all scenarios
/gov-eval --category security      # one category
/gov-eval --scenario SEC-01        # one scenario
```

Requires `MISTRAL_API_KEY`. See [`java-react/tests/`](./java-react/tests/) for full details.

**Run it on a schedule, not just once.** A rule that passes today can silently break after a model update, even with no changes to `CLAUDE.md`. Re-run GovEval on every PR touching `.claude/rules/`, and periodically (e.g. every 2 weeks) to catch drift from model updates.

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide.

Pick an open [`new-stack`](https://github.com/datallmhub/claude-governance/labels/new-stack) issue: each one is a self-contained task with clear acceptance criteria.
