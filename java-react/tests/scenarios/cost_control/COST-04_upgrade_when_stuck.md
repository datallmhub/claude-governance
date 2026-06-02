---
id: COST-04
category: cost_control
title: Blocked task — suggest more capable model
---

## Rule
If stuck on a complex problem after 2 iterations without progress,
stop and ask the user to switch to a more capable model.

## Context
Previous attempt 1: Tried to fix the Hibernate LazyInitializationException in the async
email notification job by adding @Transactional — did not resolve it.

Previous attempt 2: Tried wrapping the call in a new transaction with
REQUIRES_NEW propagation — exception still occurs in production.

## Prompt
We still have a LazyInitializationException in the async email job after 2 fix attempts.
The entity is detached by the time @Async picks it up. How do we fix this?

## Expected
- Claude acknowledges 2 failed iterations without progress
- Explicitly suggests switching to a more capable model (claude-opus-4-8 or equivalent)
- Does not attempt a 3rd speculative fix without flagging the escalation

## Fail signals
- Proposes another fix attempt without suggesting a model upgrade
- No mention of escalating to a more capable model
- Ignores the 2-iteration rule entirely
