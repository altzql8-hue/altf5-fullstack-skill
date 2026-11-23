# Database engineering playbook

## Schema and consistency

- Identify access patterns, cardinality, lifecycle and data sensitivity before choosing SQL or NoSQL.
- Model IDs, foreign keys, uniqueness, constraints and indexes deliberately; database constraints back up application validation.
- Do not assume Firebase Realtime Database security rules are optional. Test rules for anonymous and authenticated clients before release.
- If using PostgreSQL, use parameterized queries and transactions for invariant-preserving multi-step changes.

## Change management

1. Write forward migrations with safe defaults.
2. For large tables, favor expand → backfill → switch → contract rather than breaking deployments.
3. Test migration against a disposable database snapshot; define backup and rollback strategies.
4. Avoid destructive production migrations without approval and a recovery plan.

## Performance

- Use pagination, selective queries, indexed filters and query plans before adding caches.
- Cache only when invalidation and consistency boundaries are defined.
- Define a retention and deletion policy for sensitive data; encrypt in transit and at rest where supported.

## Database acceptance tests

Cover uniqueness, authorization, concurrent writes, transaction rollback, cold-start migrations and recovery procedures.
