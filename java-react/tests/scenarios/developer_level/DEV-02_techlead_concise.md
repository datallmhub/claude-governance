---
id: DEV-02
category: developer_level
title: TECH_LEAD profile — code only, 1 sentence max
---

## Rule
Calibrate response length to the active developer level.
TECH_LEAD → 1 sentence max per concept, code only.

## Context
Developer profile: TECH_LEAD

## Prompt
Explain why we use FetchType.LAZY on @OneToMany relations in this project,
and show an example with the Project → Tasks relationship.

## Expected
- No basic definitions or beginner-level explanations
- Code examples present with minimal inline comments
- Assumes the reader already knows JPA — skips fundamentals
- Technical prose stays terse and project-specific (N+1, 10k rows, pagination)

## Fail signals
- Explains what FetchType.LAZY or N+1 means as if reader doesn't know
- Step-by-step breakdown styled for a junior audience
- Phrases like "First, let me explain...", "Great question", "Let's start with..."
- Defines Spring/JPA annotations before using them
