#!/usr/bin/env python3
"""Validate starter structure and npm scripts without fetching packages."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_dir():
        return [f"not a directory: {path}"]
    manifest = path / "package.json"
    if not manifest.is_file():
        return ["missing package.json"]
    try:
        package = json.loads(manifest.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"invalid package.json: {exc}"]
    for field in ("name", "version", "scripts"):
        if not package.get(field):
            errors.append(f"missing package.json {field}")
    scripts = package.get("scripts", {})
    if not isinstance(scripts, dict):
        errors.append("scripts must be an object")
        scripts = {}
    for script in ("dev", "typecheck", "build"):
        if not scripts.get(script):
            errors.append(f"missing npm run {script}")
    for p in ("tsconfig.json", "README.md", "src"):
        if not (path / p).exists():
            errors.append(f"missing {p}")
    if "vite" in package.get("devDependencies", {}):
        if not (path / "index.html").is_file():
            errors.append("Vite template missing index.html")
    if (path / ".env").exists():
        errors.append(".env must not be included in starter templates")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    errors = validate(args.path)
    for e in errors:
        print("ERROR:", e)
    print("FAIL" if errors else f"PASS: starter project {args.path}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
