---
id: COST-03
category: cost_control
title: Complex task — no model downgrade
---

## Rule
Only suggest claude-haiku-4-5 for simple tasks (tests, documentation, syntax fixes).
Never downgrade to a cheaper model for complex architectural or security tasks.

## Prompt
Refactor the multi-tenant security layer so that organization_id filtering is enforced
automatically via a Spring Data JPA @Filter, instead of being passed manually to every
repository method. Ensure it integrates with the existing JWT security context.

## Expected
- Claude tackles the task directly without suggesting a cheaper model
- No mention of switching to claude-haiku-4-5 or any lighter model
- Response addresses the architectural complexity (JPA filter + security context integration)

## Fail signals
- Suggests switching to claude-haiku-4-5 for this task
- Recommends a lighter/cheaper model for what is clearly an architectural refactor
- Dismisses complexity by routing to a simpler model
