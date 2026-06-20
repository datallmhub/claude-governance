Initialize claude-governance for the current project.

## What this command does

1. Lists available governance stacks
2. Asks the user which stack matches their project
3. Copies the stack's CLAUDE.md, .claude/ rules, and CLAUDE.local.md.example into the current project
4. Writes a `.claude-governance` marker file so the SessionStart hook knows which stack is active

## Available stacks

| ID | Stack |
|----|-------|
| `java-react` | Java (Spring Boot 3) + React (TypeScript) |
| `react-only` | React 18 + TypeScript only |
| `angular-only` | Angular 17+ only |
| `vue-only` | Vue 3 + TypeScript only |
| `nextjs` | Next.js 14+ (full-stack) |
| `python-fastapi-react` | Python (FastAPI) + React |
| `nestjs-react` | Node.js (NestJS) + React |

## Steps

Ask the user: "Which stack are you using?" and display the table above.

Once the user selects a stack (e.g. `java-react`):

1. Locate the stack folder: it is in the same directory as this plugin (e.g. `<plugin-root>/java-react/`)
2. Copy the following into the current project root (ask for confirmation before overwriting existing files):
   - `CLAUDE.md`
   - `CLAUDE.local.md.example` (remind the user to copy it to `CLAUDE.local.md` and add it to `.gitignore`)
   - `dev-level.md`
   - `.claude/rules/` (entire folder)
   - `.claude/architecture/` (entire folder)
   - `.claude/commands/` (entire folder)
3. Write the selected stack ID into `.claude-governance` at the project root (single line, no formatting)
4. Confirm to the user:
   - Which files were copied
   - That `CLAUDE.local.md` must be created from the example and added to `.gitignore`
   - That `dev-level.md` should be updated to reflect the team's experience level
   - That governance is now active and will load automatically on every session

## Notes

- Never overwrite `CLAUDE.local.md` if it already exists — it contains personal overrides
- If `.claude-governance` already exists, show the current stack and ask if the user wants to switch
- If the stack folder does not exist yet, inform the user it is not yet available and point them to the open GitHub issue to contribute it
