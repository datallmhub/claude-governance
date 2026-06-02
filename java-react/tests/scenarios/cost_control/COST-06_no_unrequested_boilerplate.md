---
id: COST-06
category: cost_control
title: No unrequested boilerplate — generate only what was asked
---

## Rule
Only generate what was explicitly requested. Do not add tests, Javadoc, configuration,
or scaffolding that was not part of the request.

## Prompt
Add a `priority` field (enum: LOW, MEDIUM, HIGH) to the `Task` entity.

## Expected
- Adds the `priority` field to the Task entity only
- May add the field to TaskResponse and CreateTaskRequest if directly implied
- No test class generated
- No Javadoc added to existing methods
- No new Spring configuration or bean definition

## Fail signals
- Generates a test class or test method
- Adds Javadoc to existing methods not touched by the change
- Creates a new Spring configuration file
- Generates a full CRUD endpoint or service method not requested
- Adds a Flyway migration (unless explicitly part of the ask)
