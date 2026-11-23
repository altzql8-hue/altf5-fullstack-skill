#!/usr/bin/env python3
"""Execute a fixed allowlist of repository checks and record first-party observations.

This is *local test evidence*, not a signed/remote CI attestation. The program never
executes commands from a task, model response, file, or JSON manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {".git", ".artifacts", "node_modules", "dist", "coverage", "__pycache__", ".pytest_cache", ".next", ".venv"}
SECRET = re.compile(r"(?i)\b(token|password|secret|api[_-]?key)\s*[:=]\s*([\"']?)[^\s,;\"']{5,}")


def commands_for(root: Path, suite: str) -> list[tuple[str, list[str]]]:
    py = sys.executable
    core = [
        ("metadata-and-links", [py, "scripts/validate_skill.py"]),
        ("github-workflows", [py, "scripts/verify_workflows.py"]),
        ("python-unit-tests", [py, "-m", "unittest", "discover", "-s", "tests", "-v"]),
    ]
    for name in ("frontend", "threejs", "backend"):
        core += [
            (f"{name}-structure", [py, "scripts/validate_project.py", f"templates/{name}"]),
            (f"{name}-audit", [py, "scripts/audit_code.py", f"templates/{name}", "--fail-on-warning"]),
            (f"{name}-security", [py, "scripts/security_gate.py", f"templates/{name}", "--fail-on", "medium"]),
        ]
    if suite == "core":
        return core
    raise ValueError(f"unknown suite: {suite}")


def tree_digest(root: Path) -> str:
    hasher = hashlib.sha256()
    for file in sorted(root.rglob("*")):
        rel = file.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts) or file.is_symlink() or not file.is_file():
            continue
        # Ignore downloaded archives and other non-source blobs.
        if file.stat().st_size > 2_000_000:
            continue
        hasher.update(rel.as_posix().encode() + b"\x00")
        hasher.update(hashlib.sha256(file.read_bytes()).digest())
    return hasher.hexdigest()


def clean_output(value: str) -> str:
    return SECRET.sub(lambda m: m.group(1) + "=[REDACTED]", value)[-5000:]


def run(root: Path, *, timeout: int = 90) -> dict:
    if timeout <= 0 or timeout > 600:
        raise ValueError("timeout must be between 1 and 600 seconds")
    before = tree_digest(root)
    records = []
    for label, argv in commands_for(root, "core"):
        start = time.monotonic()
        try:
            result = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=timeout, shell=False)
            status, code = "passed" if result.returncode == 0 else "failed", result.returncode
            output = clean_output(result.stdout + "\n" + result.stderr)
        except subprocess.TimeoutExpired:
            status, code, output = "timed_out", None, "Command exceeded timeout"
        except OSError as exc:
            status, code, output = "not_run", None, str(exc)
        records.append({"id": label, "argv": ["python" if v == sys.executable else v for v in argv],
                        "status": status, "exit_code": code, "elapsed_ms": round((time.monotonic() - start) * 1000),
                        "output_tail": output})
    after = tree_digest(root)
    return {"schema_version": 1, "kind": "local-runner-observation", "platform": platform.system(),
            "python": platform.python_version(), "root_sha256_before": before, "root_sha256_after": after,
            "clean_tree": before == after, "passed": before == after and all(x["status"] == "passed" for x in records),
            "checks": records, "limitations": "Unsigned local observation: do not treat as authenticated CI proof."}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=Path(".artifacts/quality-report.json"))
    p.add_argument("--timeout", type=int, default=90)
    args = p.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if not output.resolve().is_relative_to(ROOT.resolve()):
        p.error("output must be inside the skill repository")
    if output.is_symlink():
        p.error("output cannot be a symbolic link")
    result = run(ROOT, timeout=args.timeout)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(output.suffix + ".tmp")
    temp.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, output)
    print(f"{sum(x['status'] == 'passed' for x in result['checks'])}/{len(result['checks'])} checks passed; clean_tree={result['clean_tree']}")
    print(f"Report: {output}")
    for record in result["checks"]:
        if record["status"] != "passed":
            print(f"FAIL {record['id']}: {record['status']}\n{record['output_tail']}")
    return int(not result["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
