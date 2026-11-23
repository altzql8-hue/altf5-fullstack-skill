# AltF5 Fullstack Engineering Skill

> An open-source Agent Skill for building reliable frontend, Three.js, and backend applications — with **working starter templates**, reference playbooks, reproducible checks, and CI.

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-24292f.svg)

## Why this exists

An AI agent should deliver working software rather than gorgeous but broken demos. This repository defines concrete build standards and ships reusable templates and validators. It **does not** retrain or replace a model and cannot guarantee code quality without testing.

## Capabilities

| Area | What the skill enforces |
| --- | --- |
| Frontend | Accessible components, responsive layouts, explicit UI states, strict TypeScript |
| Three.js | WebGL error fallback, resize lifecycle, frame-budget awareness, correct disposal |
| Backend | Validated requests, environment-based config, basic HTTP hardening, tests |
| Data | Migration safety, access controls, query efficiency, backup/recovery plans |
| Security | Secrets handling, bounded inputs, dependency and auth reviews |
| Performance | Web Vitals, bundle size limits, mobile GPU constraints, profiling |
| Operations | CI checks, deployment configuration, observability and rollback |

## Quick start

Clone/copy this repository into a supported agent's skills directory as `altf5-fullstack-engineering`, or point the agent at [`SKILL.md`](SKILL.md). See [installation instructions](docs/INSTALL.md).

```bash
# Validate the Agent Skill package (requires Python 3.10+)
python scripts/validate_skill.py
python -m unittest discover -s tests -v

# List runnable starters
python scripts/scaffold.py --list

# Create a project without modifying the template
python scripts/scaffold.py frontend ./my-frontend
cd my-frontend
npm install
npm run typecheck
npm run build
npm run dev
```

Other starters: `threejs` (interactive rotating 3D scene) and `backend` (Express 5 HTTP API). The scaffold tool will refuse to overwrite existing paths.

## Agent instructions

Ask an agent: **"Use the AltF5 Fullstack Engineering skill to make a responsive dashboard with a performant Three.js preview and a secure API. Implement and verify everything."**

For detailed process rules use [SKILL.md](SKILL.md). References are loaded when their topics become relevant, not all at once.

## Tools

```bash
python scripts/validate_skill.py
python scripts/validate_project.py templates/threejs
python scripts/audit_code.py templates/backend
python scripts/check_performance.py ./my-frontend/dist --max-total-kib 4096 --max-file-kib 1024
```

The security scanner is **heuristic**, not a replacement for an actual security review. Size checks are not frame-time benchmarks. See [quality gates](docs/QUALITY_GATES.md).

## Repository layout

```text
altf5-fullstack-engineering/
├── SKILL.md                      # Agent Skill entry point
├── references/                   # Focused agent playbooks
├── templates/
│   ├── frontend/                 # Vite + React + TypeScript
│   ├── threejs/                  # Vite + Three.js + TypeScript
│   └── backend/                  # Express + Zod + TypeScript
├── scripts/                      # Scaffold, metadata, audit, size checks
├── tests/                        # Python unit tests for the tools
├── docs/                         # Setup, recipes, design and validation
├── .github/workflows/ci.yml      # Python + Node validation in CI
└── LICENSE                       # MIT
```

## Principles

1. **Function before polish:** every interaction must work.
2. **Proof over claims:** run the checks and report their output.
3. **Secure defaults:** validate input; never trust browser input or committed secrets.
4. **Mobile-first 3D:** budget memory and pixels carefully.
5. **Progressive disclosure:** read only the needed playbook.
6. **Portable:** plain Markdown and Python scripts; no paid services necessary.

## License and contributions

MIT © AltF5 contributors. Contributions welcome; read [CONTRIBUTING.md](CONTRIBUTING.md). For private vulnerability reports, see [SECURITY.md](SECURITY.md).
