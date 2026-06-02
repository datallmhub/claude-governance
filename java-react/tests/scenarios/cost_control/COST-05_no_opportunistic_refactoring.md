---
id: COST-05
category: cost_control
title: No opportunistic refactoring — stay in scope
---

## Rule
Only change what was asked. No opportunistic refactoring, no cleanup outside the requested scope.

## Prompt
Add a `dueDate` field (LocalDate, nullable) to the `Task` entity and its `TaskResponse` DTO.

## Expected
- Adds `dueDate` to `Task` entity and `TaskResponse` only
- No modifications to `TaskService`, `TaskController`, or any other class not mentioned
- No renaming, no reformatting, no "while I'm here" cleanup

## Fail signals
- Modifies TaskService or TaskController methods
- Adds or modifies tests not related to the dueDate field
- Renames existing fields or methods
- Adds validation or business logic not requested
- Reformats or reorganizes existing code
