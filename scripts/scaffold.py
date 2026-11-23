#!/usr/bin/env python3
"""Copy a working starter into a NEW directory; never overwrite existing files."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
PROJECT_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def available() -> list[str]:
    return sorted(p.name for p in TEMPLATES.iterdir() if p.is_dir() and (p / "package.json").exists())


def scaffold(template: str, destination: Path, name: str | None = None) -> Path:
    if template not in available():
        raise ValueError(f"unknown template: {template}; available: {', '.join(available())}")
    destination = destination.expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"destination exists; refusing to overwrite: {destination}")
    project_name = name or re.sub(r"[^a-z0-9._-]+", "-", destination.name.lower()).strip("-._")
    if not PROJECT_NAME.fullmatch(project_name):
        raise ValueError("project name must be npm-safe lowercase letters, digits, '.', '_' or '-'")
    source = TEMPLATES / template
    if source.resolve() in destination.parents:
        raise ValueError("cannot scaffold inside source template directory")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("node_modules", "dist", ".env", "coverage"))
    manifest = destination / "package.json"
    package = json.loads(manifest.read_text(encoding="utf-8"))
    package["name"] = project_name
    manifest.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", nargs="?", choices=available())
    parser.add_argument("destination", nargs="?", type=Path)
    parser.add_argument("--list", action="store_true", help="show starter names")
    parser.add_argument("--name", help="override package.json package name")
    args = parser.parse_args(argv)
    if args.list:
        print("\n".join(available()))
        return 0
    if not args.template or not args.destination:
        parser.error("specify a template and destination, or use --list")
    try:
        output = scaffold(args.template, args.destination, args.name)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")
    print(f"Created {output}\nNext: cd {output} && npm install && npm run typecheck && npm run build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
