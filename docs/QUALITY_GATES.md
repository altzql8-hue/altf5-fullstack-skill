# Quality gates

A task is done only when the following are verified or explicitly reported as blocked.

| Gate | Evidence |
| --- | --- |
| Functional | Primary happy path plus error/empty/loading behavior exercised |
| Types | `npm run typecheck` passes (where applicable) |
| Build | Production `npm run build` passes |
| Tests | Relevant automated tests pass; new bug gets regression test |
| Security | No hardcoded secrets; boundary validation; authorization checked per operation |
| Accessibility | Keyboard, visible focus, labels, semantic structure and reduced-motion tested |
| Responsive | Narrow and desktop layouts both checked |
| Performance | Bundle size measured; 3D frame time profiled on target mobile hardware |
| Delivery | Setup, config, deployment, limitations and evidence documented |

## Defaults for small web apps

- Aim for reasonable Core Web Vitals (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at p75 on real user data); use these as targets, not guarantees.
- Use the included size-check script for **budget alerts**, not to infer actual load time.
- Keep mobile Three.js pixel ratio capped at 2, use modest geometry, dispose textures/materials/geometry on unmount, and load large assets deliberately.
- Do not claim security based solely on `audit_code.py` output; run dependency scans and a proper threat review.

## CI behavior

CI validates metadata, runs Python tests, statically audits all template projects, then installs each Node starter and runs its typecheck/build/tests. Build outputs are checked against size budgets. Lockfiles can be generated and committed later for repeatable application deployments; starter templates are intentionally dependency-manifest-only.
