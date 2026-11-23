# Backend API playbook

## Contracts

- Define endpoints, methods, request/response schemas, auth, error codes, and pagination before implementing controllers.
- Use separate server creation and listening logic so integration tests can import the app without opening a port.
- Validate at trust boundaries (JSON body, query, path, headers) with schema tools such as Zod.
- Return stable error shapes; avoid leaking stack traces or credentials.

## Security baseline

- Load secrets from environment or secret manager; provide examples, not real `.env` files.
- Limit request bodies, configure safe response headers, and use strict origin allowlists for browser CORS (CORS is not authorization).
- Require authorization for resource actions; verify ownership for each requested resource.
- Rate-limit expensive or sensitive endpoints; add durable/shared rate limiting for multi-instance production deployments.
- Be deliberate about trusted reverse proxies. Never blindly set `trust proxy: true`.
- Sanitize logs and redact tokens/PII. Avoid logging request bodies by default.

## Data and observability

- Give mutations idempotent behavior where reasonable; use transactions for multi-row invariants.
- Add basic health checks, request IDs, metrics and graceful shutdown.
- Prevent N+1 reads and unbounded scans; use pagination and indexed queries.

## Testing

- Happy path, malformed inputs, unauthorized and forbidden requests, rate limit, missing configuration, and dependency failure.
- Use real test clients against an isolated app; mock only external boundaries.
- Use schema-driven examples and explicit timestamps rather than brittle snapshots.

Starter: [`templates/backend`](../templates/backend/README.md).
