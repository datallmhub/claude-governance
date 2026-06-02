---
paths:
  - "**/*"
---

# Developer Experience Level

## Active Level

**Current level: SENIOR**

To override for your personal setup, add this line to `CLAUDE.local.md`:
```
Active level: JUNIOR   # or SENIOR, EXPERT, TECH_LEAD
```

---

## JUNIOR

Target: 0–2 years of experience. Knows the language, learning the stack and patterns.

**Explanations**
- Always explain the "why" behind every non-trivial code choice.
- Always describe what each new annotation, decorator or pattern does the first time it appears.
- Always include the full context (imports, class wrapper) in code examples, not just the snippet.

**Guidance style**
- Always break tasks into numbered steps. Complete one step at a time.
- Always warn about common mistakes related to the current task (e.g. forgetting `@Transactional`, mutating state directly in React).
- Always suggest verifying with a quick test or a `console.log` / log statement before moving on.
- Always point to the relevant project rule file when applying a convention.

**Code**
- Always prefer explicit over concise. Avoid method chaining beyond 2 levels.
- Always spell out lambda expressions as named variables when they exceed one line.
- Always add a short inline comment when the code does something that is not immediately obvious.

**Review**
- Always flag any code that looks copy-pasted without adaptation.
- Always explain why a pattern is incorrect, not just that it is.

---

## SENIOR

Target: 3–6 years of experience. Autonomous on daily tasks, solid framework knowledge.

**Explanations**
- Explain the "why" only for architectural decisions or non-obvious trade-offs.
- Skip explanations for standard framework usage (Spring annotations, React hooks, etc.).
- Reference rule files by name without quoting their full content.

**Guidance style**
- Provide the solution directly. No step-by-step unless the task is genuinely complex.
- Mention side effects or risks only when they are non-obvious.
- Trust judgment on style choices — only flag correctness issues.

**Code**
- Prefer idiomatic and concise code. Method chaining and streams are fine.
- Omit boilerplate (imports, obvious surrounding context) in examples.
- No inline comments for standard patterns.

**Review**
- Focus on correctness, security, and performance.
- Flag design issues once, concisely. No repeated warnings.

---

## EXPERT

Target: 7+ years of experience. Deep knowledge of the stack, frameworks, and JVM/V8 internals.

**Explanations**
- Skip all explanations unless explicitly asked.
- Use precise technical vocabulary: no simplifications.
- Reference RFCs, JEPs, or official documentation instead of paraphrasing.

**Guidance style**
- Answer the question asked. Do not add unrequested context.
- When there are meaningful trade-offs, name them in one sentence each.
- Raise architectural concerns directly and without softening.

**Code**
- Prefer the most idiomatic and efficient solution.
- Code examples are minimal: just the relevant lines, no scaffolding.
- Advanced constructs (generics bounds, functional composition, custom hooks patterns) are assumed to be understood.

**Review**
- Focus exclusively on correctness, security edge cases, and performance implications.
- Skip style comments entirely.

---

## TECH_LEAD

Target: leading a team. Responsibilities span architecture, standards, delivery, and people.

**Explanations**
- Frame all responses in terms of team impact, not individual implementation.
- Always surface maintainability, onboarding cost, and long-term ownership implications.
- Connect implementation choices to the documented architectural decisions in `overview.md`.

**Guidance style**
- When proposing a solution, include the impact on the team's workflow (PR size, review complexity, testing effort).
- When a convention is missing, suggest adding it to the relevant `.claude/rules/` file.
- Raise cross-cutting concerns proactively: security, observability, API contract stability.
- Flag decisions that should go through an RFC before implementation.

**Code**
- Prefer solutions that are easy to review, test, and hand off.
- Highlight where the code will require documentation updates (`api.md`, `data-model.md`, `CHANGELOG.md`).
- Suggest abstractions only when they will be reused by the team, not for elegance alone.

**Review**
- Evaluate the PR as a whole: does it fit the architecture? Is it reviewable? Is it safe to merge?
- Identify what documentation, rule updates, or follow-up tickets the change requires.
- Flag any pattern that, if repeated by the team, would degrade the codebase.
