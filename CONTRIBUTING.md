# Contributing to claude-governance

## What to contribute

The most valuable contributions are **new stack templates** — each open issue labeled [`new-stack`](https://github.com/datallmhub/claude-governance/labels/new-stack) is a self-contained, well-scoped task.

Other welcome contributions:
- Improvements to existing rule files (more precise rules, better examples)
- New GovEval test scenarios
- Bug fixes in `hooks/` or `.claude/commands/`

## Adding a new stack template

### 1. Pick an open issue

Each `new-stack` issue defines exactly what to build and the acceptance criteria.
Comment on the issue to claim it before starting.

### 2. Required structure

Every stack template must include all of these files:

```
<stack-name>/
├── CLAUDE.md                    # Project context + non-negotiables
├── CLAUDE.local.md.example      # Personal overrides (never committed)
├── dev-level.md                 # Active level: JUNIOR / SENIOR / EXPERT / TECH_LEAD
└── .claude/
    ├── rules/
    │   ├── backend.md           # Backend rules — scoped to backend source files
    │   ├── frontend.md          # Frontend rules — scoped to frontend source files
    │   ├── database.md          # DB / migration rules
    │   ├── testing.md           # Testing standards
    │   ├── security.md          # Security rules (loaded on every file)
    │   ├── governance.md        # Git, PR, versioning, release process
    │   └── dev-level.md        # Response format per experience level
    └── architecture/
        ├── overview.md          # System architecture + key decisions
        ├── api.md               # REST API contract
        └── data-model.md        # Database schema
```

Use [`java-react/`](./java-react/) as the reference implementation.

### Generated rule files

`governance.md`, `dev-level.md`, `security.md` and `architecture.md` are **generated** — do not edit
them inside a stack folder. `governance.md` and `dev-level.md` are compiled from `core/rules/`;
`security.md` and `architecture.md` are rendered from `policies/`, together with the matching
GitHub Copilot instruction file under `<stack>/.github/instructions/`:

```bash
tools/govctl build           # regenerate every stack
tools/govctl build --stack java-react
tools/govctl check           # fail if a generated file was hand-edited (runs in CI)
```

Stack-specific wording comes from the `vars` declared in `<stack>/govbuild.json`, and a stack
needing a whole section rewritten declares an `overlay` file whose `##` sections replace the core's.
Adding a rule that applies everywhere means editing `core/rules/`, then running `tools/govctl build`.

### Adding or changing a policy

A policy in `policies/<domain>/` carries its id, severity, enforcement surfaces, stack-agnostic
requirements, per-stack bindings and — when a deterministic check is possible — its detection
patterns. A stack opts into a policy by declaring a binding under `stacks:`; a policy that cannot
apply to a stack records the reason under `not_applicable:` rather than being silently absent.
Requirements that only hold for a stack serving HTTP go under `server_requirements:`.

Every detector must have a case in `tools/selftest.py` proving it fires on a violation, stays
silent on clean code and honours its inline waiver:

```bash
tools/selftest.py
tools/governance check --changed    # evaluate a working tree against the policies
tools/governance report --format json
```

### 3. Rules quality bar

Rules must be:
- **Stack-idiomatic** — written for the specific framework, not copy-pasted from another template
- **Imperative** — "Always use X", "Never do Y" — not "Consider using X"
- **Scoped** — backend rules must have `paths:` frontmatter targeting only backend files
- **Concrete** — include a code example for every non-obvious rule

The `CLAUDE.md` must cover at minimum:
- Tenant isolation (if multi-tenant)
- Public ID usage (UUID in URLs, never expose internal sequential ID)
- Layered architecture (controller → service → repository or equivalent)
- No secrets in code
- No unbounded collection endpoints

### 4. Test your template

Before opening a PR, verify manually that Claude Code respects the key rules:

- Open a project with your stack template
- Ask Claude to generate a basic CRUD endpoint
- Check: does the generated code use UUID in the URL? Does it avoid raw SQL? Does it respect layer separation?

If GovEval scenarios exist for your stack, run them:

```bash
cd <stack>/tests
pip install -r requirements.txt
export MISTRAL_API_KEY=sk-...
python runner.py
```

### 5. Open a PR

- Branch name: `feat/stack-<stack-name>` (e.g. `feat/stack-nestjs-react`)
- Link the PR to the corresponding issue
- Fill in the PR template

---

## PR checklist

- [ ] All required files present (7 rule files + 3 architecture docs)
- [ ] Rules are stack-idiomatic, not copy-pasted
- [ ] `paths:` frontmatter present in all scoped rule files
- [ ] `CLAUDE.local.md.example` provided
- [ ] Stack added to the table in `README.md` (status: ✅ Ready)
- [ ] Manual smoke test passed (Claude generates compliant code)

---

## Style guide for rule files

**File header** — each rule file starts with a `paths:` frontmatter block (except `security.md` and `dev-level.md` which load globally):

```markdown
---
paths:
  - backend/src/**/*.java
---

# Backend Rules — Java / Spring Boot
```

**Rule format:**

```markdown
- Always use `@Valid` on `@RequestBody` parameters.
- Never return a JPA entity directly from a controller — always map to a DTO.
```

**With code example:**

```markdown
- Always return `ResponseEntity<T>` with an explicit HTTP status.

\`\`\`java
@PostMapping
public ResponseEntity<TaskResponse> create(@Valid @RequestBody CreateTaskRequest req) {
    return ResponseEntity.status(HttpStatus.CREATED).body(taskService.create(req));
}
\`\`\`
```

**Line limit**: keep each rule file under 150 lines. Move edge cases and examples to `architecture/`.

---

## Questions

Open a [GitHub Discussion](https://github.com/datallmhub/claude-governance/discussions) for questions about scope or approach before writing code.
