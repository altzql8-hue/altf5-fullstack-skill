# AltF5 Fullstack Engineering Skill V2

[![MIT License](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-black)](SKILL.md)

**An evidence-driven engineering playbook + executable gates for coding agents building frontend, Three.js, and backend software.** Designed to reduce fabricated API claims, useless tool calls, unwanted edits, incomplete fixes, untested code and security mistakes without burning tokens on unnecessary subagents.

The skill is **not a model fine-tune or a magic hallucination remover**. It works by changing how coding agents collect evidence, implement, check and report changes. Improvement depends on the host agent actually following these instructions and running checks.

## V2's main upgrades

| Capability | Implementation |
| --- | --- |
| Symbol and dependency grounding | [Grounding playbook](references/grounding.md), [claims verifier](scripts/check_claims.py) |
| Efficient delegation | [Routing CLI](scripts/route_task.py), [subagent handoff](agents/HANDOFF.md) |
| Budgeting / trajectory visibility | [Trace grader](scripts/grade_trace.py), [efficiency guide](references/context-efficiency.md) |
| Scope control | [Diff-scope guard](scripts/check_diff_scope.py) + JSON contract |
| Defensive security | [Offline gate](scripts/security_gate.py), CodeQL, Dependabot, npm audit, ASVS checklist |
| Workflow supply-chain safety | SHA-pinned GitHub Actions, least privilege, [workflow checker](scripts/verify_workflows.py) |
| Test completeness | Negative examples, unit tests, CI matrix, [verification ladder](references/verification.md) |
| Research-based policies | [Model profiles](docs/research/MODEL_PROFILES.md), [failure taxonomy](docs/research/FAILURE_TAXONOMY.md), [sources](docs/research/SOURCES.md) |

## Quick start

Install as a skills folder named `altf5-fullstack-engineering` and tell a compatible coding agent to consult `SKILL.md`. See [installation](docs/INSTALL.md) for different agent setups.

```bash
# No third-party Python dependencies needed:
python scripts/route_task.py "Secure a frontend and backend authentication flow"
python scripts/validate_skill.py
python scripts/verify_workflows.py
python -m unittest discover -s tests -v
python scripts/check_claims.py evals/claims-example.json --root .
python scripts/grade_trace.py evals/good-trace.json
python scripts/security_gate.py templates/backend --fail-on medium

# Scaffold example application:
python scripts/scaffold.py --list
python scripts/scaffold.py threejs ./my-3d-app
cd my-3d-app && npm install && npm run typecheck && npm run build
```

For scopes:

```bash
python scripts/check_diff_scope.py --contract contracts/example-scope.json --files src/app.ts tests/app.test.ts
# Full repo diff from current Git HEAD (your project):
python scripts/check_diff_scope.py --contract contracts/example-scope.json --base HEAD
```

## How agents should work

1. **Read only relevant files**, identify actual manifest versions and symbols.
2. **Create a contract** and select one agent by default.
3. **Implement the smallest complete change**, with tests for success *and* failure cases.
4. **Run hard checks** and inspect the diff; use independent review only on meaningful risks.
5. **Report observed evidence**, not an imagined test or security result.

See [SKILL.md](SKILL.md) and [AGENTS.md](AGENTS.md) for full instructions.

## Runnable templates

- [Frontend](templates/frontend/README.md): Vite + React + TypeScript responsive starter.
- [Three.js](templates/threejs/README.md): Vite + Three.js with lifecycle cleanup and controls.
- [Backend](templates/backend/README.md): Express 5 + Zod validation, tests and basic HTTP hardening.

Templates are teaching starters, **not complete production apps**. No auth/DB infrastructure is bundled. For deployed apps, add project-specific authorization tests, secrets management, rate limits, monitoring, lockfiles and deployment configuration.

## GitHub CI and security

- [Quality gates](.github/workflows/ci.yml): stdlib unit tests, positive/negative trace fixtures, heuristic checks, typecheck/build/backend tests, npm dependency audit, asset budgets.
- [CodeQL analysis](.github/workflows/codeql.yml): Python and JS/TS security-extended analysis on PRs, main and weekly schedule.
- [Dependabot](.github/dependabot.yml): checks starter dependencies and GitHub Actions weekly.
- Action references are pinned to immutable full commit SHAs. `GITHUB_TOKEN` permissions are limited by job/workflow. CI uses `npm install` because the example starters intentionally omit lockfiles; production apps should commit lockfiles and use `npm ci`.

A clean CI run is useful evidence, not proof against every bug or vulnerability. See [security disclosure](SECURITY.md).

## Research: what should actually be measured?

An independent 2026 JetBrains Junie comparison identified different weak spots in specific GPT, Claude, Gemini and Qwen versions. These **do not** establish hard-coded traits of all later versions. See [research findings](docs/research/MODEL_PROFILES.md) and [citation notebook](docs/research/SOURCES.md). Avoid ungrounded promises like "100x better" unless you collect before/after controlled benchmarks.

## Contributing and license

MIT-licensed by AltF5 contributors. Read [CONTRIBUTING.md](CONTRIBUTING.md), and send private vulnerability reports following [SECURITY.md](SECURITY.md).
