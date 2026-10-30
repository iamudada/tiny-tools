#!/usr/bin/env python3
"""Sort files in a folder into subfolders by extension.

Default is a dry run: it only prints what it would do.
Pass --apply to actually move files. Only files directly in the
given folder are moved; subfolders are left alone.

Hidden files (names starting with ".") are skipped, and a file is
never overwritten: if the target name already exists, a numeric
suffix (_1, _2, ...) is added.

Pass --only EXT (repeatable) to tidy only files with that extension;
other files are left where they are. The extension is matched
case-insensitively, with or without a leading dot; files without an
extension match "no-extension".
"""

import argparse
import shutil
from pathlib import Path


def normalize_extensions(values):
    """Normalize extension filters to a set of bare lowercase names.

    Accepts values like "txt", ".TXT", or "no-extension". Each value may
    also be a comma-separated list. Returns an empty set for no filter.
    """
    normalized = set()
    for value in values or []:
        for part in str(value).split(","):
            part = part.strip().lower().lstrip(".")
            if part:
                normalized.add(part)
    return normalized


def unique_target(target: Path) -> Path:
    """Return target, or a numbered variant if it already exists."""
    if not target.exists():
        return target
    stem, suffix = target.stem, target.suffix
    i = 1
    while True:
        candidate = target.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def plan(folder: Path, only=None):
    """Return (source, target) moves for files in folder.

    When `only` is given (extension names, with or without a leading
    dot, case-insensitive), only files with a matching extension are
    planned; everything else is left alone.
    """
    wanted = normalize_extensions(only)
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        if item.name.startswith("."):
            continue
        ext = item.suffix.lower().lstrip(".") or "no-extension"
        if wanted and ext not in wanted:
            continue
        target = unique_target(folder / ext / item.name)
        if target != item:
            moves.append((item, target))
    return moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Folder to tidy")
    parser.add_argument("--apply", action="store_true", help="Move files (default: dry run)")
    parser.add_argument(
        "--only",
        action="append",
        metavar="EXT",
        help="Only tidy files with this extension (repeatable; dot optional, case-insensitive; use no-extension for extensionless files)",
    )
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")

    moves = plan(args.folder, only=args.only)
    if not moves:
        print("Nothing to tidy.")
        return

    for source, target in moves:
        print(f"{source.name} -> {target.parent.name}/{target.name}")

    if args.apply:
        for source, target in moves:
            target.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(target))
        print(f"Moved {len(moves)} file(s).")
    else:
        print(f"Dry run: {len(moves)} file(s) would move. Use --apply to move them.")


if __name__ == "__main__":
    main()
