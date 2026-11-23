# Application security playbook

Use defensive security practices at every trust boundary.

## Threat model

Identify assets, actors, ingress points (HTTP, WebSocket, uploads, database, dependency installs), permissions, and plausible abuse paths. Prioritize high-impact/likely cases.

## Checklist

- **Authentication:** use proven identity libraries; keep sessions/tokens out of client-visible logs and source.
- **Authorization:** verify access at each endpoint and per resource; never rely on hidden frontend buttons.
- **Validation:** bound payload sizes, validate input types and formats, use prepared SQL queries.
- **Browser:** prefer safe DOM APIs, avoid `innerHTML` with untrusted data, configure CSP intentionally.
- **Secrets:** use `.env.example` with placeholders; real secrets stay in secure hosting config and out of commits.
- **Transport:** use HTTPS in production; secure cookie flags (`HttpOnly`, `Secure`, suitable `SameSite`).
- **Dependencies:** use maintained packages and lockfiles in deployed apps; scan regularly and triage findings.
- **Telemetry:** redact auth headers, passwords, access keys, and personal identifiers.
- **Deployment:** least privilege for CI, separate staging/production config, and controlled rollbacks.

The included `audit_code.py` catches a small set of suspicious patterns and exposed `.env` files. It is a first pass, not proof of security. For a public API, perform a dedicated threat review and penetration test with explicit authorization.
