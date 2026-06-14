# Developer Experience Level

**Active level: TECH_LEAD**

Claude adapts response verbosity based on this setting.

| Level | Behavior |
|---|---|
| `JUNIOR` | Step-by-step, full context, pitfalls flagged |
| `SENIOR` | Solution-first, explain trade-offs only |
| `EXPERT` | Code only, minimal prose |
| `TECH_LEAD` | 1 sentence max per concept |

To change: edit the level above, or override in `CLAUDE.local.md`:

```
Active level: JUNIOR
```

Full level definitions: `.claude/rules/dev-level.md`.
