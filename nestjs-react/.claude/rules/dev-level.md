---
paths:
  - "**/*"
---

# Developer Experience Level

## Active Level

**Current level: TECH_LEAD**

To override for your personal setup, add this line to `CLAUDE.local.md`:
```
Active level: JUNIOR   # or SENIOR, EXPERT, TECH_LEAD
```

Or edit `dev-level.md` at the project root.

---

## JUNIOR

Target: 0–2 years of experience. Knows the language, learning the stack and patterns.

**Explanations**
- Always explain the "why" behind every non-trivial code choice.
- Always describe what each NestJS decorator or React pattern does the first time it appears.
- Always include the full context (imports, module wrapper) in code examples, not just the snippet.

**Guidance style**
- Always break tasks into numbered steps. Complete one step at a time.
- Always warn about common mistakes (forgetting `@Injectable()`, importing services across modules, mutating query cache directly).
- Always suggest verifying with a quick test or log statement before moving on.
- Always point to the relevant project rule file when applying a convention.

**Code**
- Always prefer explicit over concise. Avoid method chaining beyond 2 levels.
- Always add a short inline comment when the code does something that is not immediately obvious.

**Review**
- Always flag any code that looks copy-pasted without adaptation.
- Always explain why a pattern is incorrect, not just that it is.

---

## SENIOR

Target: 3–6 years of experience. Autonomous on daily tasks, solid framework knowledge.

**Explanations**
- Explain the "why" only for architectural decisions or non-obvious trade-offs.
- Skip explanations for standard NestJS/React usage (`@UseGuards`, hooks, etc.).
- Reference rule files by name without quoting their full content.

**Guidance style**
- Provide the solution directly. No step-by-step unless the task is genuinely complex.
- Mention side effects or risks only when they are non-obvious.
- Trust judgment on style choices — only flag correctness issues.

**Code**
- Prefer idiomatic and concise code.
- Omit boilerplate (imports, obvious surrounding context) in examples.
- No inline comments for standard patterns.

**Review**
- Focus on correctness, security, and performance.
- Flag design issues once, concisely. No repeated warnings.

---

## EXPERT

Target: 7+ years of experience. Deep knowledge of NestJS internals, TypeORM, and React.

**Explanations**
- Skip all explanations unless explicitly asked.
- Use precise technical vocabulary: no simplifications.
- Reference NestJS docs or RFCs instead of paraphrasing.

**Guidance style**
- Answer the question asked. Do not add unrequested context.
- When there are meaningful trade-offs, name them in one sentence each.
- Raise architectural concerns directly and without softening.

**Code**
- Prefer the most idiomatic and efficient solution.
- Code examples are minimal: just the relevant lines, no scaffolding.
- Advanced constructs (custom decorators, dynamic modules, query key factories) are assumed understood.

**Review**
- Focus exclusively on correctness, security edge cases, and performance implications.
- Skip style comments entirely.

---

## TECH_LEAD

Target: leading a team. Responsibilities span architecture, standards, delivery, and people.

**Response format — strictly enforced**
- 1 sentence max per concept. No prose before or after code blocks.
- No basic definitions. No step-by-step breakdowns. No filler text.
- If a risk or team impact is relevant, state it in 1 sentence — then stop.
- Assume the reader is a senior engineer: skip fundamentals entirely.
