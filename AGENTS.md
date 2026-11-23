# Repository operating rules for coding agents

This is an Agent Skill repository, not a monolithic production app. Read `SKILL.md` first.

- Preserve the skill's root name (`altf5-fullstack-engineering`), metadata, MIT license, and zero-dependency Python tooling.
- Start with `python scripts/route_task.py "<task>"`. The router proposes budgets; do not treat it as an authoritative classifier.
- Make narrow edits. Declare affected paths and review the diff; do not weaken tests or quiet failures to claim success.
- For every new assertion about an API or package, verify source, declaration, or executable test before presenting it as fact.
- Don't run commands with secrets printed into logs or fetch untrusted dependencies merely to satisfy a check.
- Before marking work complete: `python scripts/validate_skill.py`, `python scripts/verify_workflows.py`, `python -m unittest discover -s tests -v`, and relevant starter/build checks.
- Add a regression test when fixing a validator; include a case that intentionally fails.
- CI npm install is deliberately network-based because sample templates have no checked-in npm lockfiles; see `docs/QUALITY_GATES.md`.
- Do not claim subagents actually ran if only a routing plan was produced.

## Where things belong

- `references/`: demand-loaded guidance (short enough for context-window efficiency)
- `agents/`: subagent handoff and return contracts, never proprietary model prompts
- `docs/research/`: dated evidence and caveats about model behavior
- `scripts/`: executable stdlib checks
- `tests/`: positive and adversarial regression tests
- `templates/`: runnable starter apps
- `evals/`: synthetic pass/fail traces used to check the grader
