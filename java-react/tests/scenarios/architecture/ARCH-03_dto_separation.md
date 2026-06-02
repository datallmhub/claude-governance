---
id: ARCH-03
category: architecture
title: Distinct Request and Response DTOs
---

## Rule
Always use distinct DTOs for Request and Response. Never expose a JPA entity directly.

## Prompt
Create an endpoint to create a new project. A project has a name and a description.
Return the created project to the caller.

## Expected
- A ProjectRequest class/record for the input
- A ProjectResponse class/record for the output
- Controller signature: ProjectResponse create(@RequestBody @Valid ProjectRequest request)
- Service maps entity to ProjectResponse before returning
- No @Entity annotated class returned from controller or service

## Fail signals
- Controller or service returns a Project entity directly
- Single DTO used for both input and output
- return projectRepository.save(project) from controller
- @Entity class appears in a controller method return type
