# Claude Code Governance Templates

Ready-to-use Claude Code governance templates organized by tech stack.
Each subfolder is a self-contained project — copy the one that matches your stack and adapt it.

## Available stacks

| Stack | Folder | Status |
|---|---|---|
| Java (Spring Boot) + React (TypeScript) | [`java-react/`](./java-react/) | ✅ Ready |
| Java (Spring Boot) + Angular | `java-angular/` | 🔜 Coming |
| React / TypeScript only | `react-only/` | 🔜 Coming |
| Java (Spring Boot) API only | `java-only/` | 🔜 Coming |
| Python (FastAPI) + React | `python-fastapi-react/` | 🔜 Coming |

## What's inside each template

```
<stack>/
├── CLAUDE.md                    # Main project context — always loaded by Claude Code
├── CLAUDE.local.md.example      # Personal overrides template (copy → CLAUDE.local.md, do not commit)
├── .gitignore                   # Excludes CLAUDE.local.md and memory/
│
├── .claude/
│   ├── rules/
│   │   ├── backend.md           # Backend coding rules (path-scoped)
│   │   ├── frontend.md          # Frontend coding rules (path-scoped)
│   │   ├── database.md          # DB / migration rules (path-scoped)
│   │   ├── testing.md           # Testing rules (path-scoped)
│   │   ├── security.md          # Security rules (path-scoped)
│   │   ├── governance.md        # Git, PR, versioning, release rules
│   │   └── dev-level.md        # Adapt Claude's behavior to dev experience level
│   │
│   └── architecture/
│       ├── overview.md          # System architecture + key decisions
│       ├── api.md               # REST API contract
│       └── data-model.md        # Database schema
│
├── docs/
│   └── developer-guide.md       # How to use and maintain this governance system
│
└── samples/                     # Concrete code examples following the rules
```

## How to use

1. Copy the folder matching your stack into your project root.
2. Update `CLAUDE.md` with your project's actual context (name, description, stack versions).
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` and fill in your personal preferences.
4. Update `.claude/architecture/` with your actual architecture.
5. Adjust rules in `.claude/rules/` to match your team's conventions.
6. Set your experience level in `.claude/rules/dev-level.md`.

## Key concepts

### Scoped rules
Files in `.claude/rules/` use a `paths:` frontmatter that tells Claude Code when to load them:
```markdown
---
paths:
  - backend/src/**/*.java
---
```
Claude Code loads the rule file automatically when you edit a matching file.

### Developer experience levels
Edit the active level in `.claude/rules/dev-level.md`:
```
**Current level: SENIOR**
```
Or override it personally in `CLAUDE.local.md` (not committed):
```
Active level: JUNIOR
```

### Load order
```
~/.claude/CLAUDE.md        ← global personal preferences
    ↓
./CLAUDE.md                ← project rules
    ↓
./CLAUDE.local.md          ← personal overrides (gitignored)
    ↓
.claude/rules/*.md         ← path-scoped rules
```

## Contributing

PRs welcome — especially new stack templates.
Each template must follow the same folder structure and include all 7 rule files.
