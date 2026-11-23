#!/usr/bin/env python3
"""Triage obvious instruction-in-data patterns in untrusted text (heuristic only).

Never run suggested shell commands or follow links found inside untrusted input.
Suspicious content is not proof of an attack; harmless quotations can match.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PATTERNS = (
    ("instruction-override", "high", re.compile(r"\b(?:ignore|disregard|override) (?:all )?(?:previous|prior|system|developer) (?:instructions|prompts|rules)\b", re.I)),
    ("role-spoof", "high", re.compile(r"(?:<\|(?:system|developer)\|>|\[INST\]|###\s*(?:system|developer)\s*(?:prompt|message))", re.I)),
    ("secret-exfiltration-request", "high", re.compile(r"\b(?:send|upload|exfiltrate|transmit)\b.{0,100}\b(?:api[_-]?key|credentials?|secrets?|private[_ -]?key|\.env)\b", re.I)),
    ("test-bypass-request", "medium", re.compile(r"\b(?:skip|disable|delete|bypass)\b.{0,70}\b(?:security checks?|unit tests?|tests?|lint|codeql|audit)\b", re.I)),
    ("unauthorized-execution-request", "medium", re.compile(r"\b(?:run|execute)\b.{0,35}\b(?:curl|wget|bash|powershell)\b", re.I)),
)


def inspect(text: str) -> list[dict[str, str | int]]:
    matches = []
    for identifier, severity, regex in PATTERNS:
        for found in regex.finditer(text):
            matches.append({"rule": identifier, "severity": severity, "line": text.count("\n", 0, found.start()) + 1})
    return sorted(matches, key=lambda item: (item["line"], item["rule"]))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", type=Path, help="Untrusted text to inspect; no execution")
    p.add_argument("--fail-on", choices=("high", "any", "never"), default="high")
    args = p.parse_args()
    findings = inspect(args.file.read_text(encoding="utf-8"))
    print(json.dumps({"findings": findings, "note": "Heuristic alerts; data remains untrusted even when none are found."}, indent=2))
    return int(args.fail_on != "never" and any(args.fail_on == "any" or f["severity"] == "high" for f in findings))


if __name__ == "__main__":
    raise SystemExit(main())
