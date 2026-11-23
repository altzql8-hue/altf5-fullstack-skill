#!/usr/bin/env python3
"""Static guardrails for the repository's own GitHub Actions workflows (not a YAML parser)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

USE = re.compile(r"^\s*-?\s*uses:\s*(\S+)")
PINNED = re.compile(r"^[^\s@]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)?@[0-9a-f]{40}$")
UNTRUSTED = re.compile(r"\$\{\{\s*(?:github\.event\.(?:issue|pull_request|comment|head_commit)|github\.head_ref)", re.I)


def verify(workflows: Path) -> list[str]:
    problems = []
    if not workflows.is_dir():
        return ["missing workflows directory"]
    files = sorted(list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml")))
    if not files:
        return ["no workflows"]
    for file in files:
        text = file.read_text(encoding="utf-8")
        if not re.search(r"(?m)^permissions:\s*$", text):
            problems.append(f"{file.name}: missing top-level GITHUB_TOKEN permissions")
        if "pull_request_target:" in text or "workflow_run:" in text:
            problems.append(f"{file.name}: privileged trigger requires explicit manual review")
        if not re.search(r"(?m)^\s+timeout-minutes:\s+\d+", text):
            problems.append(f"{file.name}: missing job timeout-minutes")
        for lineno, line in enumerate(text.splitlines(), 1):
            match = USE.search(line)
            if match:
                spec = match.group(1)
                if not PINNED.fullmatch(spec):
                    problems.append(f"{file.name}:{lineno}: action not pinned to 40-char SHA: {spec}")
            if line.lstrip().startswith("run:") and UNTRUSTED.search(line):
                problems.append(f"{file.name}:{lineno}: untrusted event interpolation in shell command")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, nargs="?", default=Path(__file__).resolve().parent.parent / ".github" / "workflows")
    args = parser.parse_args()
    problems = verify(args.path)
    for problem in problems:
        print("FAIL:", problem)
    print(f"{'PASS' if not problems else 'FAIL'}: workflow configuration heuristics")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
