# tiny-tools

Small, dependency-free Python tools. No install, just run with Python 3.

## tidy.py

Sorts the files directly inside a folder into subfolders by extension.

```sh
# Dry run: only prints what it would do
python3 tidy.py ~/Downloads

# Actually move the files
python3 tidy.py ~/Downloads --apply

# Only tidy .txt files, leaving everything else in place
python3 tidy.py ~/Downloads --only txt --apply

# Several extensions at once (repeat --only; dot optional, case-insensitive)
python3 tidy.py ~/Downloads --only .txt --only PNG --apply
```

Subfolders are left alone. Files without an extension go into `no-extension/`.
Hidden files are skipped, and a file is never overwritten: if the target
name already exists, a suffix like `_1` is added.

## dupfind.py

Finds duplicate files in a folder by content hash (SHA-256).

```sh
# Only report duplicates
python3 dupfind.py ~/Downloads

# Delete duplicates, keeping the first file in each group
python3 dupfind.py ~/Downloads --delete
```

## Tests

```sh
python3 -m unittest discover -v
```

Tests run on every push via GitHub Actions. License: MIT.
