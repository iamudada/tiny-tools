#!/usr/bin/env python3
"""Sort files in a folder into subfolders by extension.

Default is a dry run: it only prints what it would do.
Pass --apply to actually move files. Only files directly in the
given folder are moved; subfolders are left alone.
"""

import argparse
import shutil
from pathlib import Path


def plan(folder: Path):
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        ext = item.suffix.lower().lstrip(".") or "no-extension"
        target = folder / ext / item.name
        if target != item:
            moves.append((item, target))
    return moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Folder to tidy")
    parser.add_argument("--apply", action="store_true", help="Move files (default: dry run)")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")

    moves = plan(args.folder)
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
