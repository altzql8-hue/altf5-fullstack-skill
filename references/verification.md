# Verification ladder and evidence-based exit criteria

## Start with a contract

Define observable behavior with inputs, outputs, error cases, authorization boundaries, compatibility requirements, and allowed changed paths. Record assumptions; no success claim without matching evidence.

1. Reproduce the failure or verify missing behavior against baseline.
2. Add a test that fails on old behavior when feasible, without modifying unrelated tests.
3. Implement smallest complete behavior that passes the contract.
4. Run targeted tests, strict type checking, lint, then broader regression checks proportional to scope.
5. Test negative paths: malformed JSON, missing auth, wrong tenant, boundary size, stale state, network failures, unknown routes, async race, cleanup and retries.
6. Check security and resource lifecycle. For 3D ensure disposal and context-loss behavior; for APIs ensure authorization and idempotency where applicable.
7. Inspect final diff for extra files, test weakenings, swallowed errors, synthetic fixtures or hidden behavior changes.
8. Produce a report with exact commands, exit codes, scope, uncertainty and residual risks.

## The gates

| Gate | Proof | Cannot establish |
| --- | --- | --- |
| `validate_skill.py` | Metadata and local-link presence | Semantic quality of instructions |
| `check_claims.py` | Declared files/text/packages/log format | Authentic log provenance, runtime behavior |
| `check_diff_scope.py` | Paths fall within declared contract | Correctness of changes inside paths |
| `grade_trace.py` | Recorded checks/claims/tool budgets | Whether a transcript is authentic or tests are good |
| `security_gate.py` | Obvious suspicious patterns | Absence of vulnerabilities |
| `audit_code.py` | Basic risky syntax patterns | Complete code analysis |
| `verify_workflows.py` | Pinned action refs, timeouts and minimal gate | Safe external action content |
| Tests/CI/CodeQL/npm audit | Functional and security evidence | Complete security assurance |

## Evaluating coding agents

Measure task success, test quality, unverified claims, tool retries, scope drift, reviewer-confirmed bugs and actual costs separately. Never collapse all results into a single magic "AI quality" percent. Keep positive *and* negative examples. Review false positives and false negatives; design tests independent of the patch implementation, not merely matching golden-code structure.

Sources: [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), [OpenAI benchmark validity](https://openai.com/index/separating-signal-from-noise-coding-evaluations/).
