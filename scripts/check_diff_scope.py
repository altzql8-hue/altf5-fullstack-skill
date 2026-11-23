#!/usr/bin/env python3
"""Enforce a declared set of allowed repository paths for an agent's change set.

Contract JSON: {"allowed": ["scripts/**", "tests/**"], "protected": ["LICENSE", ".github/**"]}
Uses git diff --name-only by default; --files can supply a list for deterministic testing.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) or (pattern.endswith("/**") and path == pattern[:-3]) for pattern in patterns)


def inspect_scope(changed: list[str], allowed: list[str], protected: list[str]) -> list[str]:
    problems = []
    for path in sorted(set(changed)):
        if Path(path).is_absolute() or any(part == ".." for part in Path(path).parts):
            problems.append(f"invalid changed path: {path}")
        elif not matches(path, allowed):
            problems.append(f"out-of-scope change: {path}")
        elif matches(path, protected):
            problems.append(f"protected change requires explicit owner review: {path}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--files", nargs="*", help="explicit changed paths; bypass git for fixtures")
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        allowed = contract["allowed"]
        protected = contract.get("protected", [])
        if not isinstance(allowed, list) or not all(isinstance(x, str) and x for x in allowed):
            raise ValueError("allowed must be a list of nonempty patterns")
        if not isinstance(protected, list) or not all(isinstance(x, str) for x in protected):
            raise ValueError("protected must be a list of patterns")
        changed = args.files
        if changed is None:
            result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=ACMR", args.base],
                                    capture_output=True, text=True, check=True)
            changed = result.stdout.splitlines()
        problems = inspect_scope(changed, allowed, protected)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))
    for error in problems:
        print("BLOCK:", error)
    print(f"{'PASS' if not problems else 'FAIL'}: {len(changed)} file(s) checked for scope")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
