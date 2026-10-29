# tiny-tools

One small, dependency-free Python tool to start with.

## tidy.py

Sorts the files directly inside a folder into subfolders by extension.

```sh
# Dry run: only prints what it would do
python3 tidy.py ~/Downloads

# Actually move the files
python3 tidy.py ~/Downloads --apply
```

Subfolders are left alone. Files without an extension go into `no-extension/`.
