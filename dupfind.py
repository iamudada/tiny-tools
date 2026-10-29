#!/usr/bin/env python3
"""Find duplicate files in a folder by content hash.

Groups files with identical SHA-256 hashes and prints each group.
By default it only reports; pass --delete to delete all but the
first file in each group (keeps the alphabetically first one).
Hidden files are skipped. Only files directly in the given
folder are considered; subfolders are left alone.
"""

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(folder: Path):
    groups = {}
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        groups.setdefault(sha256(item), []).append(item)
    return [g for g in groups.values() if len(g) > 1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Folder to scan")
    parser.add_argument("--delete", action="store_true",
                        help="Delete duplicates, keeping the first file in each group")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")

    groups = find_duplicates(args.folder)
    if not groups:
        print("No duplicates found.")
        return

    deleted = 0
    for group in groups:
        print("Duplicates:")
        for item in group:
            print(f"  {item.name}")
        if args.delete:
            for item in group[1:]:
                item.unlink()
                deleted += 1
    if args.delete:
        print(f"Deleted {deleted} duplicate file(s).")


if __name__ == "__main__":
    main()
