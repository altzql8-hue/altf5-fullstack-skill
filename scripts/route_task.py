#!/usr/bin/env python3
"""Deterministic, conservative delegation planner; does not run AI agents.

The planner is a guardrail and starting point, not a semantic classifier. Agents must
confirm inferred risks/areas against the actual repository before delegation.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass

AREAS = {
    "frontend": re.compile(r"\b(?:frontend|react|next(?:\.js)?|ui|ux|css|browser|accessibility|component|responsive)\b", re.I),
    "threejs": re.compile(r"\b(?:three(?:\.js)?|webgl|webgpu|shader|3d|render(?:er|ing)|gpu|scene|animation)\b", re.I),
    "backend": re.compile(r"\b(?:backend|express|fastapi|api|server|endpoint|auth(?:entication|orization)?|route)\b", re.I),
    "data": re.compile(r"\b(?:database|postgres|sql|migration|redis|firebase|rtdb|schema)\b", re.I),
    "delivery": re.compile(r"\b(?:deploy|vercel|render|ci|workflow|docker|release)\b", re.I),
}
RISKY = re.compile(r"\b(?:auth(?:entication|orization)?|permission|payment|secret|token|cryptograph|migration|public api|security|multi-tenant)\b", re.I)
SECURITY = re.compile(r"\b(?:auth(?:entication|orization)?|permission|payment|secret|token|cryptograph|security|vulnerab\w*|attack)\b", re.I)


@dataclass(frozen=True)
class Plan:
    mode: str
    domains: list[str]
    risk: str
    subagents: list[str]
    max_parallel: int
    max_total_calls: int
    max_research_calls: int
    requires_human_review: bool
    stopping_rule: str
    notes: list[str]


def plan_task(task: str, *, risk: str = "auto", max_subagents: int = 2) -> Plan:
    if not task.strip():
        raise ValueError("task must not be empty")
    if not (0 <= max_subagents <= 3):
        raise ValueError("max_subagents must be between 0 and 3")
    domains = [name for name, pattern in AREAS.items() if pattern.search(task)]
    if not domains:
        domains = ["general"]
    inferred = "high" if RISKY.search(task) else ("medium" if len(domains) >= 3 else "low")
    final_risk = inferred if risk == "auto" else risk
    if final_risk not in {"low", "medium", "high"}:
        raise ValueError("risk must be auto, low, medium, or high")

    # Delegation only for distinct, independently verifiable work. One writer owns integrations.
    eligible = len(domains) >= 2 and max_subagents > 0
    reviewers: list[str] = []
    if eligible and final_risk == "high" and SECURITY.search(task):
        reviewers.append("security-reviewer")
    if eligible and any(domain in domains for domain in ("threejs", "frontend")):
        reviewers.append("performance-accessibility-reviewer")
    if eligible and "backend" in domains and "data" in domains:
        reviewers.append("api-data-contract-reviewer")
    if eligible and not reviewers:
        reviewers.append("independent-test-designer")
    reviewers = reviewers[:max_subagents]
    mode = "single-agent" if not reviewers else "lead-with-bounded-reviewers"
    return Plan(
        mode=mode, domains=domains, risk=final_risk, subagents=reviewers,
        max_parallel=1 + len(reviewers), max_total_calls={"low": 12, "medium": 25, "high": 45}[final_risk],
        max_research_calls={"low": 3, "medium": 6, "high": 10}[final_risk],
        requires_human_review=final_risk == "high",
        stopping_rule=("Stop research when the actual symbol/contract is found and independently "
                       "verified; stop implementation once requirements and targeted tests pass. "
                       "Reopen only for a new failure or evidence."),
        notes=["Budgets are soft ceilings: request justification before exceeding them.",
               "Subagents return concise evidence (path, line, command, finding), not full transcripts.",
               "No nested delegation; only the lead agent applies changes to shared files.",
               "Always verify model-generated claims against repository and executable tests."],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="one-sentence engineering task")
    parser.add_argument("--risk", choices=["auto", "low", "medium", "high"], default="auto")
    parser.add_argument("--max-subagents", type=int, default=2)
    args = parser.parse_args()
    try:
        print(json.dumps(asdict(plan_task(args.task, risk=args.risk, max_subagents=args.max_subagents)), indent=2))
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
