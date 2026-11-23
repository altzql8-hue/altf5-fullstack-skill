# Honest measurement: quality first, efficiency second

The skill does not directly rewrite model weights. Evaluate end-to-end outcomes, not compliance with prompt wording. Model-specific performance must be assessed in the *actual* coding agent and test harness.

## Protocol for an A/B evaluation

1. Freeze a **held-out** task list with requirements, baseline commit, env/container image, tests, human-visible acceptance criteria and timeouts. Do not write tests after seeing candidate outputs.
2. Assign the same tasks to baseline (agent without the skill) and candidate (agent with V3); use the same model, effort setting, tools, and budget unless those are explicitly under test.
3. Execute independently verified tests outside the agent's writable workspace where feasible. Include negative authorization tests, boundary tests, and manual/UI reviews as appropriate; do not allow models to overwrite expected results.
4. Capture independent quality outcomes per task. Record token usage and tool calls **from actual agent telemetry**, not estimates or a model's self-report.
5. Run repeated trials with controlled random seeds where supported; report variance, failures, confidence intervals when sample size permits, and reasons for exclusions.
6. Compare matched tasks only: `python scripts/compare_eval_runs.py baseline.json candidate.json --fail-on-regression`. One task regressing is visible even if token savings look impressive.
7. Disclose: scope, date, model revision, harness, sample size, test coverage, security review process, tool telemetry quality and any unresolved findings. Never claim “100× better” without a defined measurable metric and a reproduced comparison.

Format:

```json
{"tasks":[{"id":"task-001","passed":true,"tokens":3400,"tool_calls":11}]}
```

For multiple quality dimensions, retain separate external results (functionality, security, accessibility, cost, latency, maintainability) rather than squeezing them into one pass flag. The comparison tool uses the `passed` field, so this must reflect the externally verified acceptance policy.

## Test/evidence caveats

- `scripts/run_checks.py` executes a **fixed command allowlist**, records exit codes and repository snapshots, and saves output tails to `.artifacts/`. This is stronger than manually typed 'passed=true' claims but **not cryptographically signed**. For publication, prefer official GitHub workflow runs and their immutable run IDs/commit SHAs.
- `scripts/grade_trace.py --require-runner .artifacts/quality-report.json <trace.json>` checks coherence of an attached report. A malicious actor can fabricate an unsigned JSON report. CI-run evidence, tests and independent reviewer judgment remain necessary.
- Heuristic scanners can miss vulnerabilities and produce false positives. Keep the CodeQL/dep-audit and risk-based manual review separate from functional correctness.

## References

- [OpenAI on SWE-bench Verified evaluation shortcomings (2026)](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- [SecureAgentBench: correct-and-secure agent evaluation (2025)](https://arxiv.org/abs/2509.22097)
