#!/usr/bin/env python3
"""Enforce uncompressed build-asset size budgets (not runtime performance)."""
from __future__ import annotations

import argparse
from pathlib import Path


def measure(path: Path, max_total_kib: float = 4096, max_file_kib: float = 1024) -> tuple[list[str], int, int]:
    if not path.is_dir():
        return [f"not a directory: {path}"], 0, 0
    files = [f for f in path.rglob("*") if f.is_file() and not f.is_symlink()]
    if not files:
        return [f"no build assets found: {path}"], 0, 0
    sizes = [(f, f.stat().st_size) for f in files]
    total = sum(size for _, size in sizes)
    errors = []
    for filename, size in sizes:
        if size > max_file_kib * 1024:
            errors.append(f"asset over {max_file_kib:g} KiB: {filename} ({size / 1024:.1f} KiB)")
    if total > max_total_kib * 1024:
        errors.append(f"total over {max_total_kib:g} KiB: {total / 1024:.1f} KiB")
    return errors, total, len(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--max-total-kib", type=float, default=4096)
    parser.add_argument("--max-file-kib", type=float, default=1024)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args(argv)
    if args.max_total_kib <= 0 or args.max_file_kib <= 0:
        parser.error("budgets must be positive")
    errors, total, count = measure(args.path, args.max_total_kib, args.max_file_kib)
    print(f"Build assets: {count} file(s), {total / 1024:.1f} KiB total (uncompressed)")
    for error in errors:
        print("BUDGET:", error)
    print("PASS" if not errors else ("WARN" if args.warn_only else "FAIL"))
    return int(bool(errors) and not args.warn_only)


if __name__ == "__main__":
    raise SystemExit(main())
