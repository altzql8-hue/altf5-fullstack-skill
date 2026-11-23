# Minimal subagent handoff (use only when router justifies it)

Lead agent owns the requirement contract, integration, all shared-file edits, testing and final claims. Subagents work read-only unless isolated branch/worktree explicitly assigned. Never delegate a task merely to 'think harder'.

## Dispatch contract

```json
{
  "role": "security-reviewer",
  "goal": "Review authentication boundary for concrete regressions",
  "scope": ["src/auth/**", "tests/auth/**"],
  "inputs": ["authenticated-user contract", "changed diff"],
  "excluded": ["unrelated refactors", "production secrets"],
  "max_tool_calls": 6,
  "max_output_tokens": 500,
  "must_return": ["severity", "reproduction or evidence", "file:line", "minimal fix"],
  "stop_when": "reviewed changed trust boundaries and found no more actionable evidence"
}
```

## Response contract

Return a concise table or JSON: `{finding, severity, path, line, evidence, confidence, recommended_change}`. Say `none found` if none. Report unknowns, not speculation. Output file paths and command results instead of pasted whole source files. Stop once focused evidence is exhausted; no nested agents. The lead revalidates every finding.

## Priority

1. Required functional fix and tests.
2. Independent review of security/performance when risk justifies it.
3. Optional parallel discovery on distinct components when context is genuinely large.
4. No delegation on small tasks; cheaper, faster and usually clearer.
