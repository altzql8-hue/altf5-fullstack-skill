# Installation

The skill follows the [Agent Skills specification](https://agentskills.io/specification). The folder name must be `altf5-fullstack-engineering` to match the YAML `name` in `SKILL.md`.

## Per-project (agents that scan `.agents/skills/`)

```bash
mkdir -p .agents/skills
# Copy the WHOLE altf5-fullstack-engineering directory here:
cp -R /path/to/altf5-fullstack-engineering .agents/skills/
```

The exact discovery path differs by coding agent; consult that agent's documentation. Alternatively, tell your agent to read `SKILL.md` directly. Keep `references/`, `scripts/`, and `templates/` alongside it.

## Requirements

- Python 3.10+ for the stdlib-only validators and scaffolder.
- Node.js 22+ and npm for the optional TypeScript starter projects.
- No paid services are required.

## Validate

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/scaffold.py --list
```

## Try the examples

```bash
python scripts/scaffold.py threejs ./demo-3d
cd demo-3d
npm install
npm run typecheck
npm run build
npm run dev
```

For APIs use `backend`; copy `.env.example` to `.env` before starting, and review deployment settings before production.
