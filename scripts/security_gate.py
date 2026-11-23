#!/usr/bin/env python3
"""Small offline security guardrail for obvious high-risk configurations and snippets.

This is an additional smoke check, NOT SAST or a vulnerability assessment.
Patterns deliberately require tight signal to avoid reporting all safe examples.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

IGNORE = {".git", "node_modules", "dist", "coverage", ".next", "__pycache__", "vendor"}
SOURCE_EXT = {".js", ".jsx", ".ts", ".tsx", ".py", ".json", ".yml", ".yaml"}
RULES = [
    ("disabled-tls-verification", "high", re.compile(r"\bNODE_TLS_REJECT_UNAUTHORIZED\s*[:=]\s*['\"]?0\b|\bverify\s*=\s*False\b")),
    ("weak-jwt-algorithm", "high", re.compile(r"\balgorithms?\s*[:=]\s*\[?\s*['\"]none['\"]", re.I)),
    ("credentialed-wildcard-cors", "high", re.compile(r"(?:credentials\s*:\s*true.{0,160}origin\s*:\s*['\"]\*|origin\s*:\s*['\"]\*.{0,160}credentials\s*:\s*true)")),
    ("unsafe-eval", "medium", re.compile(r"\beval\s*\(|\bnew\s+Function\s*\(")),
    ("insecure-crypto-random", "medium", re.compile(r"\bMath\.random\(\).*\b(?:token|secret|password|key)\b|\b(?:token|secret|password|key)\b.*\bMath\.random\(\)", re.I)),
    ("insecure-temp-file", "medium", re.compile(r"\btempfile\.mktemp\(")),
]

@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    path: str
    line: int
    message: str


def scan(root: Path) -> list[Finding]:
    output: list[Finding] = []
    iterator = [root] if root.is_file() else root.rglob("*")
    for file in iterator:
        if not file.is_file() or file.is_symlink() or any(part in IGNORE for part in file.parts):
            continue
        display = str(file.relative_to(root)) if root.is_dir() else file.name
        if file.name in {".env", ".env.production", ".env.local"} or file.suffix in {".pem", ".p12", ".pfx", ".key"}:
            output.append(Finding("sensitive-file", "high", display, 0, "Remove from source control; rotate if disclosed"))
            continue
        if file.suffix not in SOURCE_EXT:
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if file.stat().st_size > 1_000_000:
            continue
        for rule, severity, regex in RULES:
            for match in regex.finditer(text):
                before = text.rfind("\n", 0, match.start())
                # Ignore single-line comments; review multi-line comments manually.
                if text[before + 1:match.start()].lstrip().startswith(("//", "#", "*")):
                    continue
                output.append(Finding(rule, severity, display, text.count("\n", 0, match.start()) + 1,
                                      "Review unsafe or questionable security pattern"))
    return sorted(output, key=lambda x: (x.path, x.line, x.rule))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--fail-on", choices=["high", "medium", "never"], default="high")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.root.exists():
        parser.error("root path not found")
    findings = scan(args.root)
    if args.json:
        print(json.dumps({"findings": [asdict(x) for x in findings], "count": len(findings)}, indent=2))
    else:
        for item in findings:
            print(f"{item.severity.upper()} {item.path}:{item.line} [{item.rule}] {item.message}")
        print(f"Offline security gate: {len(findings)} heuristic finding(s); run CodeQL + dependency scans too")
    return int(any(args.fail_on != "never" and (item.severity == "high" or args.fail_on == "medium") for item in findings))


if __name__ == "__main__":
    raise SystemExit(main())
