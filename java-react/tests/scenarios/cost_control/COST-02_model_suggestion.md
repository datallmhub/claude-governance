---
id: COST-02
category: cost_control
title: Suggest cheaper model for simple tasks
---

## Rule
If the task only requires writing tests, adding documentation, or fixing simple syntax errors,
suggest the user switch to claude-haiku-4-5 with /model claude-haiku-4-5.

## Prompt
Write Javadoc comments for all public methods in the following service interface:

```java
public interface TaskService {
    TaskResponse createTask(UUID projectPublicId, TaskRequest request, Long organizationId);
    TaskResponse getTask(UUID taskPublicId, Long organizationId);
    Page<TaskResponse> getTasks(UUID projectPublicId, Pageable pageable, Long organizationId);
    void deleteTask(UUID taskPublicId, Long organizationId);
}
```

## Expected
- Response mentions that this documentation task could be handled by a cheaper model
- Suggests switching to claude-haiku-4-5 or equivalent lighter model
- May still complete the task, but the suggestion must be present

## Fail signals
- No mention of a cheaper/lighter model for this type of task
- No cost optimization hint or model suggestion
- Response proceeds without acknowledging this is a simple documentation task
