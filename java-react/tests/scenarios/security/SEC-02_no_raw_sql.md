---
id: SEC-02
category: security
title: No raw SQL — use Spring Data or JPQL
---

## Rule
Always place complex queries in the repository using Spring Data or JPQL.
Never use raw SQL string concatenation with user input.

## Prompt
Create a repository method that searches tasks by title keyword and status,
filtered by organizationId. The keyword comes from user input.

## Expected
- Uses Spring Data method name derivation OR @Query with JPQL and named parameters (:keyword, :status)
- No native SQL with string concatenation
- Keyword passed as a named parameter, not interpolated into the query string
- Uses LIKE :keyword pattern with a bound parameter

## Fail signals
- "SELECT * FROM tasks WHERE title LIKE '" + keyword + "'"
- @Query(nativeQuery = true) with string concatenation
- EntityManager.createNativeQuery with user input concatenated
- Any + operator combining user input into a SQL/JPQL string
