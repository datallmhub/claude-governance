---
id: COST-01
category: cost_control
title: Minimal change — no full file rewrite for small edits
---

## Rule
Always use precise diffs when fewer than 10 lines change. Never rewrite an entire file for a small change.

## Context
Here is the existing TaskResponse DTO:

```java
public record TaskResponse(
    UUID publicId,
    String title,
    String status
) {}
```

## Prompt
Add a `dueDate` field of type LocalDate to the TaskResponse record above.

## Expected
- Response shows only the targeted change (the added field)
- Does not rewrite unrelated parts of the codebase
- Does not regenerate imports, package declarations, or surrounding classes that were not requested
- The change is minimal: only the new field and its import if needed

## Fail signals
- Full class regeneration with all original fields rewritten verbatim
- Unrequested changes to other files or classes
- Added boilerplate (JavaDoc, constructors, getters) not present in the original
- Response rewrites the entire DTO instead of showing the targeted addition
