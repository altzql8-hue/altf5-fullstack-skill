#!/usr/bin/env python3
"""Validate basic Agent Skills metadata and local Markdown links, using stdlib only."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def parse_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    marker = content.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("SKILL.md frontmatter is missing a closing ---")
    result: dict[str, str] = {}
    # Accept simple scalar fields and nested metadata; no dependency on PyYAML.
    for line in content[4:marker].splitlines():
        if not line or line.isspace() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        match = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            result[key] = value.strip().strip('"\'')
    return result


def validate(root: Path, *, check_directory_name: bool = True) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return [f"missing: {skill}"]
    try:
        fields = parse_frontmatter(skill.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        return [str(exc)]
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not (1 <= len(name) <= 64) or not NAME_RE.fullmatch(name):
        errors.append("invalid name: expected 1–64 lowercase kebab-case characters")
    if check_directory_name and name != root.name:
        errors.append(f"name '{name}' must match parent directory '{root.name}'")
    if not (1 <= len(desc) <= 1024):
        errors.append("description must be between 1 and 1024 characters")
    if not fields.get("license"):
        errors.append("missing license metadata")
    if not (root / "LICENSE").exists():
        errors.append("missing LICENSE")
    # Check all local Markdown links (no external resources fetched).
    for markdown in root.rglob("*.md"):
        if any(part.startswith(".") and part != ".github" for part in markdown.relative_to(root).parts):
            continue
        content = markdown.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(content):
            raw = match.group(1).strip().split(" ", 1)[0].strip("<>")
            if not raw or raw.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            path = unquote(raw.split("#", 1)[0].split("?", 1)[0])
            if not (markdown.parent / path).exists():
                errors.append(f"broken local link {markdown.relative_to(root)} -> {raw}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--repository-checkout", action="store_true",
                        help="Skip only the folder-name comparison for a GitHub checkout with a different repo slug")
    args = parser.parse_args(argv)
    errors = validate(args.root.resolve(), check_directory_name=not args.repository_checkout)
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    if errors:
        print(f"FAIL: {len(errors)} skill validation issue(s)")
        return 1
    print("PASS: Agent Skill metadata, naming, license and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
