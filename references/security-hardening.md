# Security review checklist (defensive engineering)

Use for exposed APIs, multi-tenant access, authentication, payments, uploads and supply-chain changes. Maintain a threat model with assets, trust boundaries, attacker-controlled inputs and abuse cases. Start with [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) and map relevant implementation controls to [OWASP ASVS 5.0](https://asvs.owasp.org/).

## API and data boundaries

- Object authorization on **every** server-side record and endpoint; do not infer authorization from a client-provided user ID or filtered UI.
- Validate path/query/body at ingress, limit size and content types; parameterize SQL, bound query pagination and use safe file-path handling.
- Separate authentication (identity) from authorization (per resource permission). Use short-lived credentials, established session libraries and explicit revocation/rotation.
- CSRF defenses for cookie-authenticated state changes; secure cookie attributes, CORS allowlist, security headers. Never use wildcard CORS together with credentials.
- File uploads: inspect metadata and content, enforce sizes and storage isolation; never trust filenames or extensions.
- SSRF: outbound fetch allowlist and destination validation; restrict redirects and internal/private endpoints.
- Secrets only in secret managers or environment variables; strip errors, logs and stack traces of tokens and private data.
- Timeouts, rate limits, circuit breakers and bounds for external calls. Monitor unusual behavior without logging sensitive request bodies.

## Toolchain and CI

- Run offline guards, CodeQL, dependency vulnerability checks and secret scanning where available; review each finding manually.
- Keep `GITHUB_TOKEN` least-privileged, pin action releases to full commit SHAs, avoid privileged PR triggers, and treat third-party actions as code executing in your runner.
- Include negative authorization and malformed-input tests. A clean grep is not a security certification; human review is required for high-impact changes.
- Scope review explicitly includes admin/API key management, key-generation endpoints, signature validation and user-controlled redirection when applicable.

Run `python scripts/security_gate.py <project> --fail-on medium`; this script intentionally makes no claim to be full SAST. Run `python scripts/audit_code.py <project> --fail-on-warning`, then actual dependency audits and CodeQL in CI.
