# V3 research findings (reviewed 2026-11-23)

## Motivation

Evidence from contemporary evaluations supports separating **functionality**, **security**, and **efficiency** in AI coding systems:

- [SecureAgentBench (2025)](https://arxiv.org/abs/2509.22097): real-world vulnerability tasks showed correct-but-insecure solutions, with additional security instructions alone offering limited improvement. Hence V3 runs explicit scanners and mandates independent negative/security tests rather than merely saying “write secure code”.
- [Last Secure Code Benchmark (October 2026)](https://arxiv.org/abs/2610.14766): broad task and language coverage showed substantial gaps between passing functionality checks and passing both functionality and security. These model/harness-dependent measurements do **not** establish a fixed insecurity rate for any deployed model.
- [OpenAI on SWE-bench Verified limitations (February 2026)](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/): test flaws, contamination and grading constraints can distort single-number coding claims. V3 requires held-out acceptance tests and a fixed before/after task set.
- [Task-grounded reasoning failures (October 2026)](https://arxiv.org/abs/2610.32338): code-agent trajectories can contain incorrect concrete claims about tasks/code; V3 prioritizes repository evidence, actual runs and narrow context rather than self-declared correctness.
- [Coding-agent security threat survey (2026)](https://www.sciencedirect.com/science/article/pii/S0950584926002776): tool results and malicious repository content form distinct lower-trust entry points. V3 includes untrusted-context instructions and a heuristic triage checker.
- [OWASP GitHub Actions Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html): full-SHA action pinning, least privilege and avoiding direct interpolation of untrusted event fields into shell are important. V3 inspects multi-line run blocks and CI preserves run evidence.

## Practical changes and limits

| Failure mode | New control | What remains unsolved |
| --- | --- | --- |
| Agent claims it ran tests without running them | `run_checks.py` executes fixed commands and records status/output | Local JSON is unsigned; rely on trusted CI for strong provenance |
| Unsafe injected instructions inside repo/web content | `check_context.py`, lower-trust handling guide | Lexical detection is incomplete, may flag harmless quotes |
| Excessive repository reading | `context_plan.py` recommends paths within approximate context budget | Does not understand semantics or measure actual tokenizer usage |
| Incomparable benchmark task sets | `compare_eval_runs.py` requires equal task IDs and exposes regressions | Supplied quality flags/usage must come from independent telemetry |
| Workflow shell interpolation hidden in YAML multi-line blocks | Updated `verify_workflows.py` and regression tests | Not a full YAML AST or taint-flow analyzer |
| Dependency drift | Explicit lockfile requirement for release/production | Examples still lack npm lockfiles; GitHub `npm install` remains registry-dependent |

**Do not confuse more rules or more tests with proven model improvement.** Evaluate the same hidden tasks and measure verified quality, security and cost over repeated trials.
