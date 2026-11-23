#!/usr/bin/env python3
"""Verify claim evidence against local files and saved command results, without executing commands.

Claims JSON: {"claims": [{"id":"...","type":"file_exists|contains_text|command_passed|package_declared",
"path":"relative/path","text":"...","log":"relative/log.json","package":"zod"}]}
Command log JSON: {"command":"npm test", "exit_code":0, "stdout":"...", "stderr":"..."}
A passing command log is an *attestation*, not proof it was executed; trusted CI must create it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED = {"file_exists", "contains_text", "command_passed", "package_declared"}


def confined(root: Path, name: str) -> Path:
    if not name or Path(name).is_absolute():
        raise ValueError("paths must be non-empty and relative")
    resolved = (root / name).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("path leaves the verification root")
    return resolved


def check_claims(root: Path, claims: list[dict[str, Any]]) -> list[dict[str, str | bool]]:
    results: list[dict[str, str | bool]] = []
    for index, item in enumerate(claims):
        identifier = str(item.get("id", f"claim-{index + 1}"))
        kind = item.get("type")
        try:
            if kind not in ALLOWED:
                raise ValueError(f"unknown claim type: {kind}")
            if kind == "command_passed":
                evidence = json.loads(confined(root, str(item.get("log", ""))).read_text(encoding="utf-8"))
                expected = str(item.get("command", ""))
                ok = bool(expected and evidence.get("command") == expected and
                          type(evidence.get("exit_code")) is int and evidence["exit_code"] == 0)
                detail = "matching recorded command exit_code=0" if ok else "command log does not match passing command"
            else:
                path = confined(root, str(item.get("path", "")))
                if kind == "file_exists":
                    ok = path.is_file()
                    detail = "file present" if ok else "file missing"
                elif kind == "contains_text":
                    value = item.get("text")
                    if not isinstance(value, str) or not value:
                        raise ValueError("contains_text needs nonempty text")
                    ok = path.is_file() and value in path.read_text(encoding="utf-8")
                    detail = "text found" if ok else "text not found"
                else:
                    pkg = item.get("package")
                    if not isinstance(pkg, str) or not pkg:
                        raise ValueError("package_declared needs package")
                    manifest = json.loads(path.read_text(encoding="utf-8"))
                    ok = any(pkg in manifest.get(section, {}) for section in ("dependencies", "devDependencies", "peerDependencies"))
                    detail = "package declared" if ok else "package not declared"
        except (OSError, UnicodeError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            ok, detail = False, f"invalid/missing evidence: {exc}"
        results.append({"id": identifier, "pass": ok, "detail": detail})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="path to claims.json")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        payload = json.loads(args.manifest.read_text(encoding="utf-8"))
        claims = payload["claims"]
        if not isinstance(claims, list) or not claims:
            raise ValueError("claims must be a nonempty array")
        results = check_claims(args.root.resolve(), claims)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps({"passed": sum(x["pass"] for x in results), "total": len(results), "results": results}, indent=2))
    return int(not all(x["pass"] for x in results))


if __name__ == "__main__":
    raise SystemExit(main())
