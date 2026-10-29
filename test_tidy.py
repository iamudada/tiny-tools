import unittest
from pathlib import Path
import tempfile

from tidy import plan, unique_target


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


if __name__ == "__main__":
    unittest.main()
