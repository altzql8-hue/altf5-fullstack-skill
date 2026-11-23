#!/usr/bin/env python3
"""Heuristic code audit; helps flag common hazards but is NOT a security scanner."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

EXCLUDE_DIRS = {"node_modules", "dist", ".git", "coverage", "__pycache__"}
SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".py"}
PATTERNS = {
    "dynamic-eval": re.compile(r"\beval\s*\("),
    "dynamic-function": re.compile(r"\bnew\s+Function\s*\("),
    "dom-html-injection": re.compile(r"\.innerHTML\s*=|dangerouslySetInnerHTML"),
    "shell-command": re.compile(r"\bshell\s*=\s*True|\bchild_process\.exec\s*\("),
    "hardcoded-secret": re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|password|access[_-]?token)\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"),
}


@dataclass(frozen=True)
class Finding:
    filename: str
    line: int
    rule: str
    severity: str


def audit(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    files = [path] if path.is_file() else path.rglob("*")
    for file in files:
        if any(part in EXCLUDE_DIRS for part in file.parts) or not file.is_file() or file.is_symlink():
            continue
        if file.name == ".env" or (file.name.startswith(".env.") and not file.name.endswith(".example")):
            findings.append(Finding(str(file), 0, "committed-env-file", "ERROR"))
            continue
        if file.suffix not in SUFFIXES:
            continue
        try:
            lines = file.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith(("//", "#", "*")):
                continue
            for rule, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(str(file), i, rule, "WARNING"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(argv)
    if not args.path.exists():
        parser.error(f"path does not exist: {args.path}")
    findings = audit(args.path)
    for finding in findings:
        print(f"{finding.severity}: {finding.filename}:{finding.line} [{finding.rule}]")
    print(f"Audit: {len(findings)} heuristic finding(s); manual review still required")
    return int(any(f.severity == "ERROR" or args.fail_on_warning for f in findings))


if __name__ == "__main__":
    raise SystemExit(main())
