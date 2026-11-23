# Deployment and operations playbook

## Release readiness

- Build in CI, test exact commit, and keep secrets in the deployment platform rather than checked-in files.
- Use fixed Node/Python versions and dependency lockfiles for production apps.
- Use HTTPS, health probes, structured logs, and reasonable resource/time budgets.
- Verify staging deployment against real auth, CORS and database rules before promoting to production.

## Vercel / static frontend

- Build Vite output to `dist`; configure the hosting build command and output directory.
- Never expose server-side secrets in client bundles. Variables prefixed `VITE_` are visible to users by design.
- Configure fallback routing only when using client-side routes; don't blindly redirect API calls to index.html.

## Render / Node backend

- Set the start command to `npm run start` after building; provide `PORT`, `ALLOWED_ORIGIN`, and any required service secrets as environment values.
- Configure health checks against `/health` and assess reverse-proxy settings before trusting forwarded headers.
- Use a persistent store if runtime state must survive restart or horizontal scaling; in-memory rate limits are per instance.

## Rollback and incident response

Keep artifact IDs and migration versions, predefine rollback windows, monitor error rates and user-critical operations, and have a simple procedure to restore a known-good release. Avoid destructive database operations in a fast rollback.
