# Subagent decision policy — bounded by expected value

**Default:** one lead agent. Parallel readers are useful only for independent questions, not tightly coupled shared implementation. The router in `scripts/route_task.py` is an advisory heuristic, not a model dispatcher.

## When to delegate

| Situation | Number of delegated specialists | Example deliverable |
| --- | ---: | --- |
| One-file UI fix or CSS polish | 0 | One focused diff + screenshot/test |
| Frontend/API contract mismatch | 1 | Read-only contract review with exact code references |
| Authentication across frontend/backend/data | 1–2 | Negative authorization test plan and independent security risk review |
| Performance investigation with measured bottleneck | 1 | Profiler hypotheses ranked by expected impact |
| No isolated deliverable, no evidence, or overlapping edits | 0 | Keep with lead; avoid wasted tokens |

## Efficient handoff template

```text
Task: One narrowly bounded question
Allowed read paths: relative paths only; no secrets
Output: at most 8 concise findings with path/line + test/evidence + confidence
Budget: <tool-call ceiling> + <token ceiling from host telemetry>
Forbidden: code writes; running unreviewed third-party scripts; recursive delegation
Return: findings, unresolved assumptions, suggested verification, stop reason
```

Never hand off all previous chat messages by default. Send a minimal problem statement, precise files and required interface contract. The lead remains the only writer/integrator.

## Termination

Stop researching after finding the concrete symbol/contract and one independent confirmation, unless security risk calls for extra checking. Stop delegating if reviewers duplicate work, exceed a declared budget, or fail to produce unique evidence. Do not spawn a second agent to ask a question the lead can answer with one direct tool call.

## What the scripts can and cannot control

`route_task.py` **suggests** agents, call ceilings and research ceilings; `context_plan.py` suggests files to inspect by cheap path-level relevance; `grade_trace.py` summarizes supplied telemetry. None of them controls actual model tokens, spawns agents, or enforces hosted pricing limits. The host agent's orchestration controls must implement real ceilings.

## Why

Research on multi-agent systems finds token overhead can be large and extra agents are not automatically useful for sequential, interdependent coding. See [Anthropic's multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) and [building effective agents](https://www.anthropic.com/research/building-effective-agents).
