# Contributing

Contributions should solve observed problems, not just add longer prompts. Before PRs, read [SKILL.md](SKILL.md), [research sources](docs/research/SOURCES.md) and [quality gates](docs/QUALITY_GATES.md).

1. Explain the failure mode, measurable acceptance criterion and changed-file scope.
2. For new scripts, include at least one expected-pass and one expected-fail test. Keep Python tools compatible with 3.10+ stdlib.
3. Run `python scripts/validate_skill.py`, `python scripts/verify_workflows.py` and `python -m unittest discover -s tests -v`.
4. For templates, verify strict typing, build, existing tests and a security/dependency review.
5. Link research sources with date, evaluated models and harness. No claims that a provider universally hallucinates more from one benchmark.
6. Don't include credentials, unlicensed code, production datasets or attack payloads.
7. Record exact commands run and failures; do not weaken tests or falsify logs to make a PR green.

Pull requests should be focused; protected authentication, supply-chain and CI paths warrant independent review.
