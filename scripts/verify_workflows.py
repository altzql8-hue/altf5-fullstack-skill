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
        lines = text.splitlines()
        if not re.search(r"(?m)^permissions:\s*$", text):
            problems.append(f"{file.name}: missing top-level GITHUB_TOKEN permissions")
        if re.search(r"(?m)^\s*(?:pull_request_target|workflow_run):", text):
            problems.append(f"{file.name}: privileged trigger requires explicit manual review")
        if not re.search(r"(?m)^\s+timeout-minutes:\s+\d+", text):
            problems.append(f"{file.name}: missing job timeout-minutes")
        if re.search(r"(?m)^permissions:\s*write-all\s*$", text):
            problems.append(f"{file.name}: broad write-all token permissions")
        if re.search(r"(?m)^\s*persist-credentials:\s*true\s*$", text):
            problems.append(f"{file.name}: checkout credentials persisted")
        # Inspect entire multi-line run/env blocks, not just the literal 'run:' line.
        # This is lexical policy checking, not a complete YAML/dataflow parser.
        watch_indent = None
        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            if watch_indent is not None and indent <= watch_indent:
                watch_indent = None
            key_match = re.match(r"^\s*(?:-\s*)?(run|env):(?:\s|$)", line)
            if key_match:
                watch_indent = indent
            if watch_indent is not None and UNTRUSTED.search(line):
                problems.append(f"{file.name}:{lineno}: untrusted event interpolation in shell/env context")
        for lineno, line in enumerate(lines, 1):
            match = USE.search(line)
            if match:
                spec = match.group(1)
                if not PINNED.fullmatch(spec):
                    problems.append(f"{file.name}:{lineno}: action not pinned to 40-char SHA: {spec}")
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
