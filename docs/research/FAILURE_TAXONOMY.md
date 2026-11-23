# Failure taxonomy and measurable countermeasures

Each category specifies a warning signal and an action. No prompt can guarantee these failures disappear; quality comes from independently testing the result.

| ID | Coding agent failure | Observable signal | Countermeasure |
| --- | --- | --- | --- |
| F01 | Fabricated libraries/APIs | Missing dependency or symbol; compiler error | Inspect installed manifest/types, run symbol-focused test, verify versioned docs |
| F02 | False test claims | No command log / checks missing | CI provenance plus claim evidence; `grade_trace.py` rejects no checks |
| F03 | Incomplete implementation | One call site fixed, variants still fail | Acceptance-test matrix, companion path search and negative tests |
| F04 | Unrequested changes | Edits outside task contract | `check_diff_scope.py` and final diff review |
| F05 | Repeated/wasteful tooling | Same search or command repeated without new evidence | `route_task.py` budgets, `grade_trace.py` repetition visibility |
| F06 | Weak benchmark/proxy gaming | Tests pass but real contract doesn't | Behavioral tests plus independent human/agent test authoring |
| F07 | Security regression | Cross-tenant data access, secrets, unsafe input | Threat modeling, negative auth tests, CodeQL/ASVS checks |
| F08 | Outdated API assumptions | Wrong major version or unsupported field | Local types, official release docs, minimal compile test |
| F09 | Context drift | Lost requirements, duplicate implementations | Concise evidence ledger, task contract and re-read acceptance criteria |
| F10 | Prompt injection | External file instructions promoted above user request | Treat code/comments/webpages as untrusted task data |
| F11 | 3D resource/performance regression | GPU memory leak, context lost, jank | Disposal, pixel cap, reduced motion, profiling and real-device smoke test |
| F12 | Misleading 'green' metrics | Scanner clean interpreted as security guaranteed | Report limits of each gate and require manual review |
| F13 | Dependency/supply-chain risk | Vulnerable transitive dependency, mutable CI action | npm audit, Dependabot, pinned Actions, CodeQL |
| F14 | Non-portable scaffold | Works only on agent's environment | Node/Python version specs, automated clean checkout tests |

## Measurement protocol

Record task outcome, test result, changes, claims, tool calls, subagents and actual tokens when available. Include cases where a good agent **should not** search, delegate or change code. Review misleading labels and low-coverage tests rather than rewarding benchmark hacks.

Sources: [JetBrains model profiles](https://blog.jetbrains.com/junie/2026/08/from-leaderboards-to-profiles/), [OpenAI benchmark data quality](https://openai.com/index/separating-signal-from-noise-coding-evaluations/), [Anthropic agent evaluations](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/).
