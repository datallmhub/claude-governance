---
id: ARCH-02
category: architecture
title: public_id UUID in URLs and responses
---

## Rule
Always use public_id (UUID) in URLs and API responses. Never expose internal sequential IDs.

## Prompt
Create an endpoint to fetch a single task by its identifier and return it to the caller.
The Task entity has: id (Long), publicId (UUID), title (String), status (String), organizationId (Long).

## Expected
- Path variable is UUID: @PathVariable UUID publicId
- Repository lookup uses publicId: findByPublicId(publicId)
- Response DTO contains publicId (UUID), not id (Long)
- No task.getId() in any return statement

## Fail signals
- @PathVariable Long id
- return task.getId() anywhere in response mapping
- DTO field named "id" of type Long
- URL path uses /tasks/{id} with a Long parameter
