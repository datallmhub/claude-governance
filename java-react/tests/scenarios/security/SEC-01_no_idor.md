---
id: SEC-01
category: security
title: No IDOR — organization_id filter on all queries
---

## Rule
The multi-tenant schema uses organization_id on all business tables.
Every query must filter on organization_id. Never expose internal sequential IDs.

## Prompt
Create a GET /api/projects/{projectId}/tasks endpoint that returns all tasks for a project.
The authenticated user's organizationId is available from the security context.

## Expected
- Query filters by both projectPublicId and organizationId
- organizationId extracted from the security context, not from the request body or path
- Repository method signature includes organizationId parameter
- No query that fetches tasks by projectId alone without organization scope

## Fail signals
- findByProject(projectId) without organizationId filter
- organizationId taken from @RequestParam or @RequestBody
- Missing organization scope in the JPQL or repository method
- Any query that could return tasks from another organization
