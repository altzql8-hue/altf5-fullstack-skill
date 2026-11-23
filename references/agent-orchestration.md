# Efficient agent and subagent orchestration

Read this only for tasks spanning multiple independent components or requiring an independent reviewer. **Single agent is the default**; the skill is not a runtime or subagent launcher.

## Budgeted strategy

Run `python scripts/route_task.py "<task>" --risk auto --max-subagents 2` for a conservative starting budget. Then confirm domains against the repository. The router emits a plan, not live agents, token measurements, or a judgment of model competence.

| Task | Approach | Delegation |
| --- | --- | --- |
| One route, component or bug | Single agent | None |
| Unfamiliar repo | Lead with bounded navigation | Optional one read-only explorer |
| UI + 3D + API | Lead owns integration | Independent UI/performance reviewer and API security reviewer |
| Auth, payment, migration | Lead + explicit risk review | One security reviewer if separate scope; human approval |
| Large independent documents | Parallel reading with compressed findings | Maximum two peers by default |

No one should spawn subagents just to brainstorm generic ideas. Subagents are appropriate when **expected error reduction or elapsed-time savings exceeds coordination/token cost**. A research system can benefit from broad parallelization; a tightly coupled code change often cannot. Do not use subagents for trivial questions, overlapping file edits or redundant searches.

## Handoff and communication

Use [agents/HANDOFF.md](../agents/HANDOFF.md) for every delegated task. Supply objective, exact file scope, expected artifact, max calls/output and stop rule. For shared files, allow only the lead to edit. Independent reviewers return *findings* with paths, lines, reproduction, and confidence, not hundreds of lines of pasted code.

Hard gates:

1. No nested subagents; no unbounded self-delegation.
2. Research budget: one targeted symbol search, follow references, verify docs/types; stop if contract found.
3. Stop searching when there's enough evidence to implement. Reopen only on a contradiction or failing test.
4. Never ask another agent to repeat an identical task without specifying a different input, test, or falsification criterion.
5. Use cheapest sufficient capability for deterministic linting and triage; use the strongest available reasoning model for real ambiguity. Never claim a specific provider is always best without task-local evidence.
6. Discard low-confidence, unsupported agent findings rather than propagating them into the lead's response.

## Context compression

- Keep a 200–500 word state: goal, decisions, verified symbols, changed paths, test status, outstanding risks.
- Return code pointers instead of dumping files. Prefer `rg -n`, symbol lookups and targeted ranges over full trees or repeated web searches.
- Reuse cached verified dependency/API notes inside the task; invalidate them when manifest or library version changes.
- Assign different reviewer perspectives only when independence improves accuracy, e.g. security vs rendering performance.
- Report actual token/cost figures only if the harness exposes usage logs; budgets without measurements are estimates.

## Sources

[Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents), [Anthropic: multi-agent research tradeoffs](https://www.anthropic.com/research/multi-agent-research-system), [Anthropic: context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents).
