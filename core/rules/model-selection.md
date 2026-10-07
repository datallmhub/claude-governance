---
paths:
  - "**/*"
---

# Model Selection

Model switching is manual. Suggest `/model` when the task warrants it:

| Task type | Suggestion |
|-----------|------------|
| {{LIGHT_TASKS}} | Suggest `/model claude-haiku-4-5` |
| Feature dev, bug fix, architecture (default) | Stay on `claude-sonnet-5-5` |
| Blocked after 2 attempts, security review | Suggest `/model claude-opus-5-5` |

- If stuck after 2 failed attempts on the same problem: stop and tell the user to run `/model claude-opus-5-5`.
- Never suggest the lighter model for work touching {{SENSITIVE_AREAS}}.
