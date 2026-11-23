---
name: altf5-fullstack-engineering
description: Evidence-driven, usage-efficient engineering for frontend, Three.js and backend work. Use to implement, debug, audit and improve full-stack apps with grounded API/package claims, bounded subagents, scope controls, risk-based testing, defensive security review, performance budgets, and honest execution evidence.
license: MIT
compatibility: Python 3.10+ for stdlib tools; optional Node.js 22+ for example apps. Works as portable Agent Skills instructions with tools available in the host coding agent.
metadata:
  author: AltF5
  version: "2.0.0"
  category: development
---

# AltF5 Fullstack Engineering — evidence-first V2

**Goal:** Deliver a *complete, testable, secure-by-design implementation with minimal necessary tokens, calls and changes*. This skill provides instructions and offline checks; it does not secretly modify models, launch subagents, enforce API billing limits, or guarantee vulnerability-free code.

## Non-negotiable operating rules

1. **Trust evidence, not plausibility.** Never invent an existing API, npm package, option, path, benchmark result, build outcome, quote, or source. Verify new library symbols against installed code/types/versioned docs, then compile or smoke-test. See [grounding](references/grounding.md).
2. **Single agent by default.** Run `python scripts/route_task.py "<task>"` for suggested scope and budgets. Delegate only independent, scoped reviews where benefits justify cost; max two peers by default, no nested delegation. See [orchestration](references/agent-orchestration.md) and [handoff](agents/HANDOFF.md).
3. **Preserve scope.** Before edits define behavior, allowed paths, success criteria, and tests. Do not rewrite unrelated files, rewrite tests to hide failures, or suppress exceptions to claim success. Use [scope checks](scripts/check_diff_scope.py).
4. **Executable validation.** 'Pass' means a real, observed check passed. Run smallest useful failing test first, then types, build, relevant regressions and risk-based security/performance checks. Never claim CI is green before reading its actual result. See [verification](references/verification.md).
5. **Security is a separate dimension.** Audit trust boundaries, authorization, injection, supply chain, secrets and default configurations; use [security guidance](references/security-hardening.md). Clean heuristic results are not proof of security.
6. **Stop when finished.** No endless searching, spawning, polishing or unrelated infrastructure repair. Use context summaries, direct code pointers and targeted checks. See [efficiency](references/context-efficiency.md).
7. **No dishonest output.** State exactly what was run, what was not run, limitations and residual risk. If blocked, report a concrete partial result rather than inventing success.

## Operational workflow

### A. Triage (small effort)

- Read `AGENTS.md` and existing README, manifests, relevant code, CI, and recent changes. Confirm user goal and non-goals; preserve current architecture unless change is required.
- Route area(s): [frontend](references/frontend.md), [Three.js](references/threejs.md), [backend](references/backend.md), [database](references/database.md), [deployment](references/deployment.md), [design](references/design-system.md), [performance](references/performance.md), and/or [security](references/security.md).
- For unfamiliar/model-dependent software behavior, consult [grounding](references/grounding.md) *before* modifying files. For model-profile nuances and dated source limitations, see [model profiles](docs/research/MODEL_PROFILES.md).
- Create a minimal contract: desired observable outcome, allowed changed paths, main risks, smallest executable test, rollback and necessary approvals.

### B. Choose workflow proportional to risk

| Risk | Typical change | Workflow | Reviewer |
| --- | --- | --- | --- |
| Low | Copy/UI adjustments, isolated refactor | Single agent, targeted check | No extra agent |
| Medium | Cross-component change | One lead, contract tests, independent review only if useful | At most one or two read-only subagents |
| High | Auth, tenancy, data migrations, credentials, payments | Threat model, negative cases, broader tests, human approval | Independent security reviewer when possible |

Subagents must not own shared-file merges; only the lead integrates. Router estimates are *policy suggestions*, not measured tokens or usage caps.

### C. Implement a complete vertical slice

- Follow project conventions; implement all requested wired interactions, not fake controls or stubs.
- Frontend: responsive, accessible, keyboard-friendly and explicit loading/empty/error/success states.
- Three.js: lifecycle disposal, pixel ratio limits, resize/context handling, GPU and asset budgets, mobile fallbacks.
- Backend: structured input validation, per-object authorization where required, bounded payloads, clear errors and safe deployment configuration.
- Data: migrations with rollback plan, tested permission boundaries and backups.
- Update tests and docs only where behavior/contract actually changed.

### D. Independently verify

Run relevant tooling and capture exact outcomes:

```bash
python scripts/validate_skill.py
python scripts/verify_workflows.py
python -m unittest discover -s tests -v
python scripts/validate_project.py templates/backend
python scripts/audit_code.py templates/backend --fail-on-warning
python scripts/security_gate.py templates/backend --fail-on medium
python scripts/check_claims.py evals/claims-example.json --root .
python scripts/grade_trace.py evals/good-trace.json
```

For actual projects, run their native typecheck, tests, build, dependency audit and relevant smoke or performance measurements; on CI inspect CodeQL. Use `python scripts/check_performance.py <dist>` only for uncompressed bundle size, not FPS. When npm dependencies are available, starter checks are typecheck/build/tests as declared in each manifest.

### E. Deliver an evidence report

Report: changed files, acceptance criteria tested, exact commands + outcomes, security concerns reviewed, unverified assumptions, anything not executed and run/deploy instructions. Do not assert that an evaluation harness itself improved model accuracy without an independent before/after benchmark.

## Read-on-demand directory

- [Research: coding agent failure taxonomy](docs/research/FAILURE_TAXONOMY.md)
- [Research: evaluated model-specific patterns](docs/research/MODEL_PROFILES.md)
- [Research: cited sources and limits](docs/research/SOURCES.md)
- [Agent handoff format](agents/HANDOFF.md)
- [Quality gates and threat model](docs/QUALITY_GATES.md)
- [Install and use the skill](docs/INSTALL.md)
- [Starter templates](templates/)
