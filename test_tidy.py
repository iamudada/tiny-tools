import subprocess
import sys
import unittest
from pathlib import Path
import tempfile

from tidy import normalize_extensions, plan, unique_target


class TestTidy(unittest.TestCase):
    def test_plan_groups_by_extension(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("a")
            (folder / "b.png").write_text("b")
            moves = plan(folder)
            self.assertEqual(
                sorted(str(t.relative_to(folder)) for _, t in moves),
                ["png/b.png", "txt/a.txt"],
            )

    def test_hidden_files_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / ".hidden.txt").write_text("x")
            self.assertEqual(plan(folder), [])

    def test_unique_target_avoids_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "txt").mkdir()
            (folder / "txt" / "a.txt").write_text("old")
            target = unique_target(folder / "txt" / "a.txt")
            self.assertEqual(target.name, "a_1.txt")

    def test_only_filters_to_given_extension(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("a")
            (folder / "b.txt").write_text("b")
            (folder / "c.png").write_text("c")
            moves = plan(folder, only=["txt"])
            self.assertEqual(
                sorted(str(t.relative_to(folder)) for _, t in moves),
                ["txt/a.txt", "txt/b.txt"],
            )

    def test_only_accepts_dot_and_uppercase(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("a")
            (folder / "b.PNG").write_text("b")
            moves = plan(folder, only=[".TXT"])
            self.assertEqual(
                [str(t.relative_to(folder)) for _, t in moves], ["txt/a.txt"]
            )
            self.assertEqual(normalize_extensions([".TXT", "png, jpg"]), {"txt", "png", "jpg"})

    def test_only_multiple_extensions(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("a")
            (folder / "b.png").write_text("b")
            (folder / "c.md").write_text("c")
            moves = plan(folder, only=["txt", "png"])
            self.assertEqual(
                sorted(str(t.relative_to(folder)) for _, t in moves),
                ["png/b.png", "txt/a.txt"],
            )

    def test_only_no_match_returns_empty(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("a")
            self.assertEqual(plan(folder, only=["png"]), [])

    def test_only_no_extension_keyword(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "README").write_text("r")
            (folder / "a.txt").write_text("a")
            moves = plan(folder, only=["no-extension"])
            self.assertEqual(
                [str(t.relative_to(folder)) for _, t in moves],
                ["no-extension/README"],
            )

    def test_cli_only_apply_moves_only_matching_files(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("a")
            (folder / "b.png").write_text("b")
            script = Path(__file__).with_name("tidy.py")
            result = subprocess.run(
                [sys.executable, str(script), str(folder), "--only", "txt", "--apply"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((folder / "txt" / "a.txt").exists())
            self.assertTrue((folder / "b.png").exists())
            self.assertFalse((folder / "a.txt").exists())


if __name__ == "__main__":
    unittest.main()
