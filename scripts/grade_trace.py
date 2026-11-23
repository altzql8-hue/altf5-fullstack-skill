#!/usr/bin/env python3
"""Score structured agent traces; reports observable evidence, not hidden reasoning.

Trace JSON schema: {"task":"...", "claims":[{"verified":true}], "tools":[{"name":"...", "signature":"..."}],
"changes":["..."], "checks":[{"name":"...", "passed":true}], "subagents":[{"task":"..."}]}
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def grade(trace: dict[str, Any], *, max_tools: int = 30, max_agents: int = 2, require_runner: bool = False, runner_report: dict[str, Any] | None = None) -> dict[str, Any]:
    tools = trace.get("tools", [])
    claims = trace.get("claims", [])
    checks = trace.get("checks", [])
    agents = trace.get("subagents", [])
    if not all(isinstance(x, list) for x in [tools, claims, checks, agents]):
        raise ValueError("tools/claims/checks/subagents must be arrays")
    if max_tools < 1 or max_agents < 0:
        raise ValueError("invalid budgets")
    signatures = [str(x.get("signature", x.get("name", ""))) for x in tools]
    repetitions = sum(v - 1 for v in Counter(signatures).values() if v > 1)
    unsupported = sum(1 for x in claims if x.get("verified") is not True)
    failed_checks = sum(1 for x in checks if x.get("passed") is not True)
    checks_ok = bool(checks) and failed_checks == 0
    budgets_ok = len(tools) <= max_tools and len(agents) <= max_agents
    runner_ok = bool(runner_report and runner_report.get("kind") == "local-runner-observation"
                     and runner_report.get("passed") is True
                     and runner_report.get("clean_tree") is True
                     and runner_report.get("root_sha256_before") == runner_report.get("root_sha256_after")
                     and isinstance(runner_report.get("checks"), list) and runner_report["checks"]
                     and all(isinstance(x, dict) and x.get("status") == "passed" for x in runner_report["checks"]))
    outcome = checks_ok and unsupported == 0 and budgets_ok and (not require_runner or runner_ok)
    return {
        "pass": outcome,
        "checks_present": bool(checks),
        "checks_passed": len(checks) - failed_checks,
        "checks_failed_or_unknown": failed_checks,
        "unverified_claims": unsupported,
        "tool_calls": len(tools),
        "duplicate_tool_signatures": repetitions,
        "subagents": len(agents),
        "budgets_ok": budgets_ok,
        "runner_report_present": runner_report is not None,
        "runner_checks_passed": runner_ok,
        "warnings": (["No executable checks recorded"] if not checks else []) +
                    (["Repeated tool call signatures: investigate redundant exploration"] if repetitions else []) +
                    (["Runner evidence absent or invalid"] if require_runner and not runner_ok else []) +
                    (["Self-reported trace fields are not authenticated evidence"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--max-tools", type=int, default=30)
    parser.add_argument("--max-subagents", type=int, default=2)
    parser.add_argument("--require-runner", type=Path, help="Require locally captured suite report (not signed CI)")
    args = parser.parse_args()
    try:
        trace = json.loads(args.trace.read_text(encoding="utf-8"))
        runner_report = json.loads(args.require_runner.read_text(encoding="utf-8")) if args.require_runner else None
        result = grade(trace, max_tools=args.max_tools, max_agents=args.max_subagents,
                       require_runner=bool(args.require_runner), runner_report=runner_report)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return int(not result["pass"])


if __name__ == "__main__":
    raise SystemExit(main())
