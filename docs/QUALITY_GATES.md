# Quality gates — measurable, risk-based, not magical

| Area | Entry check | Exit check | Escalation |
| --- | --- | --- | --- |
| Scope | Define allowed paths/contracts | `check_diff_scope.py` and manual diff review | Changes to auth, secrets, workflow or data paths need owner review |
| Correctness | Reproduce baseline; acceptance criteria | Targeted tests -> types/build -> broader regression tests | Unreproduced issue or incomplete integration |
| Grounding | Inspect packages, type declarations, docs | `check_claims.py` + real typecheck | Unverified external APIs or log provenance |
| Security | List trust boundaries and sensitive data | `security_gate.py`, `audit_code.py`, CodeQL, npm audit | Authorization flaws, token leakage or high-severity findings |
| Efficiency | `route_task.py` for budgeted planning | `grade_trace.py` and repeat-call review | Max calls exceeded without new evidence |
| Delivery | Confirm runtime and environment | Smoke test, deploy/rollback notes, honest report | Any test not executed must be explicitly named |
| 3D rendering | Asset/visual quality requirements | WebGL context fallback, cleanup, bundle size and device test | Shader/VRAM/performance failures |

## Executable local checks

```bash
python scripts/validate_skill.py
python scripts/verify_workflows.py
python -m unittest discover -s tests -v
python scripts/check_claims.py evals/claims-example.json --root .
python scripts/grade_trace.py evals/good-trace.json
python scripts/validate_project.py templates/frontend
python scripts/validate_project.py templates/threejs
python scripts/validate_project.py templates/backend
python scripts/audit_code.py templates/backend --fail-on-warning
python scripts/security_gate.py templates/backend --fail-on medium
```

**Negative test:** `python scripts/grade_trace.py evals/bad-trace.json` should return a nonzero exit. A successful synthetic test only proves the scoring script's logic on that fixture.

## CI limitations

The sample templates do not yet carry npm lockfiles, so CI uses `npm install`; those installs are not fully reproducible. Production projects should **commit a package lock and use `npm ci`**. Dependency audit results depend on npm registry availability and advisory freshness. CodeQL and the local regex-based checks do not cover every possible flaw; security-critical changes need manual review.

## Honest agent metrics

Evaluate against a baseline set of real tasks, repeat each trial, and report passing runtime behavior, extra files touched, hallucinated symbols, tool calls, tokens/cost (only if measured), reviewer time and vulnerabilities separately. Avoid percentage claims until observed. Keep failures, false alarms and changing harness configurations in the record.
