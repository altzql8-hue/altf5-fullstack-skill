# Token and tool economy

**Efficiency means minimum evidence-gathering work needed for a reliable result, not skipping checks.**

## Information retrieval

- Start from manifest, route files, failing test and likely symbols. Use paths/line-numbered excerpts rather than reading entire large files.
- Search once by primary identifier, then narrower by call-site/dependency; record the result in a small evidence ledger. Stop repeated equivalent searches.
- Use official version-specific documentation only for unfamiliar/changing APIs. Avoid browsing for stable, locally inspectable behavior.
- Don't repeatedly run full suites while debugging one small change; run failing test then the relevant broader suite once at finish.
- Use deterministic Python/TypeScript scripts rather than calling a new LLM to count files, compare paths, parse logs or score trace signals.

## Subagent policy

- One lead by default. Delegate one **read-only, independent** review if risk warrants; two subagents only for genuinely separate domains.
- Limit prompts to scoped evidence and requested decision. Every extra agent needs a separate task and measurable success condition.
- Prefer two independent negative tests to three agents arguing over the same implementation.
- Time and money budgets require actual provider usage data; a router's `max_total_calls` is a policy suggestion, not a billing cap.

## Stop rules

The lead can stop when the written contract is implemented, targeted and broad relevant checks pass, no unresolved high-severity risk remains, and any lack of coverage is disclosed. Do not invent 'one last improvement' after meeting requirements. If the next exploration is unlikely to change the decision, stop.
