---
id: ARCH-01
category: architecture
title: Layer separation — DELETE endpoint
---

## Rule
Controllers hold no business logic — delegate everything to the service.
Golden rule: controller → service → repository. No layer skipping.

## Prompt
Create a DELETE /api/tasks/{publicId} endpoint.
The task can only be deleted if it belongs to the authenticated user's organization.
The Task entity has: id (Long), publicId (UUID), organizationId (Long).

## Expected
- Controller delegates entirely to TaskService
- Ownership check lives in the service, not the controller
- Repository call is in the service only
- Controller method body is at most 2 lines (call service + return)

## Fail signals
- taskRepository called directly from the controller
- if/else or ownership check logic in the controller method
- Business exception thrown from the controller
