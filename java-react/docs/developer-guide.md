# Developer Guide — Claude Code Governance with CLAUDE.md

## What is this system?

This repository contains the Claude Code governance system for the TaskFlow project.
It structures how Claude Code understands and operates within the project through a hierarchy of configuration files.

---

## File Hierarchy

```
~/.claude/CLAUDE.md              ← Level 1: personal preferences (not shared)
    ↓
./CLAUDE.md                      ← Level 2: project rules (shared via Git)
    ↓
./module/CLAUDE.md               ← Level 3: sub-module rules (shared)
    ↓
.claude/rules/*.md               ← Level 4: path-scoped rules
    ↓
CLAUDE.local.md                  ← Level 5: personal overrides (not shared)
```

**On conflict**: the most specific rule wins.
Project rules take precedence over personal preferences for security and architecture.

**Official load order** (from broadest to most specific):
1. Managed policy (`/etc/claude-code/CLAUDE.md`) — enterprise/institution level
2. `~/.claude/CLAUDE.md` — global user preferences
3. `./CLAUDE.md` — project rules
4. `./CLAUDE.local.md` — personal local overrides
5. `.claude/rules/*.md` — path-scoped rules (loaded when matching files are accessed)
6. Auto memory — first 200 lines or 25KB

---

## Repository Structure

```
claude-config/
│
├── CLAUDE.md                    # Main entry point — always loaded
├── CLAUDE.local.md              # Not committed (.gitignore) — personal overrides
│
├── .claude/
│   ├── rules/
│   │   ├── backend.md           # Loaded for: backend/src/**/*.java
│   │   ├── frontend.md          # Loaded for: frontend/src/**/*.tsx, *.ts
│   │   ├── database.md          # Loaded for: **/*Repository*.java, migrations/**
│   │   └── testing.md           # Loaded for: src/test/**/*.java, *.test.ts
│   │
│   └── architecture/
│       ├── overview.md          # System overview
│       ├── api.md               # REST API + WebSocket contract
│       └── data-model.md        # Database schema
│
└── docs/
    └── guide-developpeurs.md    # This file
```

---

## How to Use This System

### Set up a new project

1. Copy this repository as a base or use it as a reference.
2. Update `CLAUDE.md` with your project's context.
3. Adapt rules in `.claude/rules/` to your stack.
4. Create `CLAUDE.local.md` locally (do not commit).
5. Verify `CLAUDE.local.md` is in `.gitignore`.

### Add a rule for a new domain

1. Create `.claude/rules/mydomain.md`.
2. Declare the `paths:` frontmatter at the top of the file (before the title):
   ```
   ---
   paths:
     - src/mymodule/**/*.java
   ---
   ```
3. Write rules in imperative form, short and unambiguous.
4. Commit to the project repository.

### Update an existing rule

- Edit the relevant file directly in `.claude/rules/`.
- Delete obsolete rules rather than commenting them out.
- Keep each file under 200 lines (official Claude Code limit).

### Document a technical decision

Add a section in `.claude/architecture/overview.md` with:
- The decision
- The reason
- The consequences for day-to-day development

---

## Writing Good Rules

### Use positive imperatives

```
✓  Always use shadcn/ui components for UI elements.
✗  Consider using shadcn/ui when possible.
✗  Don't use raw HTML elements.  ← negative framing
```

### One rule = one measurable behavior

```
✓  Always use FetchType.LAZY on @OneToMany relations.
✗  Avoid JPA performance issues.
```

### Include a code example for non-obvious rules

```java
// Correct
@Transactional(readOnly = true)
public TaskResponse findByPublicId(UUID publicId) {
    return taskRepository.findByPublicId(publicId)
        .map(mapper::toResponse)
        .orElseThrow(() -> new TaskNotFoundException(publicId));
}
```

---

## What Claude Code Gets From This System

| Situation                             | Expected behavior                                        |
|---------------------------------------|----------------------------------------------------------|
| Creating a Spring service             | Applies naming conventions, `@Transactional`, DTOs       |
| Adding a React component              | Uses shadcn/ui, TanStack Query, strict TypeScript        |
| Writing a SQL migration               | Follows Flyway naming, adds indexes, filters org_id      |
| Writing a test                        | Chooses the right level (unit / integration / Testcontainers) |
| Modifying a JPA entity                | Creates a Flyway migration, never modifies schema in code|
| Proposing a new endpoint              | Follows REST conventions from `api.md`, uses UUID        |

---

## Maintaining the System

### Recommended update cadence

- After every architecture decision: update `overview.md`.
- After every convention validated in code review: add to the relevant rule file.
- Quarterly: review all rules and remove outdated ones.

### Signals that a rule is needed

- Claude Code makes the same mistake repeatedly.
- The same code review comment keeps coming up.
- Onboarding reveals a recurring misunderstanding of the architecture.

### Signals that a rule should be deleted

- The stack changed (e.g. migrating from Zustand to Jotai).
- The rule has become obvious and adds no value.
- The file exceeds 200 lines — split or clean up.

---

## Recommended .gitignore

```gitignore
# Personal Claude Code governance files
CLAUDE.local.md
.claude/memory/
```

`CLAUDE.md`, `.claude/rules/` and `.claude/architecture/` are **always committed**.
