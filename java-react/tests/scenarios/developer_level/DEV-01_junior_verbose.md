---
id: DEV-01
category: developer_level
title: JUNIOR profile — full explanation expected
---

## Rule
Calibrate response length to the active developer level.
JUNIOR → full explanation allowed, step-by-step reasoning.

## Context
Developer profile: JUNIOR

## Prompt
Explain why we use FetchType.LAZY on @OneToMany relations in this project,
and show an example with the Project → Tasks relationship.

## Expected
- Detailed explanation of what LAZY loading means
- Explains the N+1 problem and why LAZY avoids it by default
- Shows a code example with @OneToMany(fetch = FetchType.LAZY)
- Explains when to use explicit fetch joins
- Response is multi-paragraph, educational in tone

## Fail signals
- Response is a single sentence with no explanation
- No code example provided
- No explanation of why, only what
- Response length appropriate for TECH_LEAD but not for JUNIOR
