---
name: altf5-fullstack-engineering
description: Build, repair, review, and optimize production-quality frontend, Three.js/WebGL, and backend projects. Use when an agent needs a structured implementation workflow, accessible responsive UI, performant 3D graphics, secure APIs, practical starter templates, measurable quality gates, or deployment readiness checks.
license: MIT
compatibility: Requires Python 3.10+ for included validators; Node.js 22+ and npm for optional starter templates. Instructions work with any coding agent supporting Agent Skills.
metadata:
  author: AltF5
  version: "1.0.0"
  category: development
---

# AltF5 Fullstack Engineering

Use this skill to deliver **working software**, not just mockups or impressive-looking code. Follow this workflow and read the relevant reference files on demand.

## 1. Discover and choose a path

1. Examine the existing codebase, scripts, dependencies, constraints, runtime, and user expectations. Do not overwrite working configuration.
2. Identify the requested work: UI, 3D graphics, API, database, deployment, review, or multiple.
3. Select only the relevant references:
   - Frontend & accessibility: [references/frontend.md](references/frontend.md) and [references/design-system.md](references/design-system.md)
   - Three.js / shaders: [references/threejs.md](references/threejs.md)
   - APIs and validation: [references/backend.md](references/backend.md)
   - Persistence and migrations: [references/database.md](references/database.md)
   - Threat modeling & secrets: [references/security.md](references/security.md)
   - Bundles, frame time, Web Vitals: [references/performance.md](references/performance.md)
   - Release & operations: [references/deployment.md](references/deployment.md)
4. For new projects, prefer a small proven stack. Use `python scripts/scaffold.py --list` to see templates.

## 2. Plan before implementation

Write a concise change plan stating affected files, API contracts, user flows, risks, tests, and success criteria. For short tasks, keep this to a few sentences. For ambiguous tasks, make explicit reversible assumptions and continue.

## 3. Implement with production standards

- Build vertical slices that run end-to-end; do not leave fake buttons, stub handlers, or disconnected frontend/backend flows.
- Use strict typing and clear naming; handle loading, empty, error, and success states.
- Validate untrusted input at the boundary; restrict CORS appropriately; never hardcode credentials.
- Preserve keyboard access, visible focus, semantic labels, reduced-motion support, and mobile layouts.
- For Three.js: lifecycle cleanup, renderer resize, pixel ratio caps, asset budgets, controls, and context-failure fallback are mandatory.
- Avoid premature complexity; isolate I/O, put configuration in environment variables, and document assumptions.

## 4. Verify, measure, and fix

Run the tests the project already has. For new templates:

```bash
python scripts/validate_skill.py
python scripts/validate_project.py templates/frontend
python scripts/validate_project.py templates/threejs
python scripts/validate_project.py templates/backend
python -m unittest discover -s tests -v
```

Where dependencies are available, run each template's `npm install`, `npm run typecheck`, `npm run build`, and `npm test` where defined. Inspect warnings and regressions, not merely exit status. Audit security-sensitive changes with `python scripts/audit_code.py <path>`. For built frontend assets use `python scripts/check_performance.py <path>/dist`.

## 5. Report concrete evidence

Provide a change summary, exact commands run and their outcomes, unresolved concerns, and deployment instructions. Never claim tests/builds pass without executing them. Do not expose secrets or private files. If requested delivery is impossible, ship the functioning local artifact and disclose the blocker.

## References and starters

- [Installation](docs/INSTALL.md)
- [Quality gates](docs/QUALITY_GATES.md)
- [Design recipes](docs/RECIPES.md)
- [Starter templates](templates/)
- [Contributing](CONTRIBUTING.md)
