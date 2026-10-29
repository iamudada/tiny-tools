import unittest
from pathlib import Path
import tempfile

from dupfind import find_duplicates


class TestDupfind(unittest.TestCase):
    def test_finds_duplicates_by_content(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("same")
            (folder / "b.txt").write_text("same")
            (folder / "c.txt").write_text("different")
            groups = find_duplicates(folder)
            self.assertEqual(len(groups), 1)
            self.assertEqual([p.name for p in groups[0]], ["a.txt", "b.txt"])

    def test_no_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            (folder / "a.txt").write_text("one")
            (folder / "b.txt").write_text("two")
            self.assertEqual(find_duplicates(folder), [])


if __name__ == "__main__":
    unittest.main()
