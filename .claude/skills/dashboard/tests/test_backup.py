import unittest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from backup import backup_file


class TestBackup(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_creates_bak_file(self):
        src = self.root / 'agent.md'
        src.write_text('original content')
        bak_path = backup_file(src)
        self.assertTrue(Path(bak_path).exists())
        self.assertEqual(Path(bak_path).read_text(), 'original content')

    def test_bak_path_has_timestamp(self):
        src = self.root / 'agent.md'
        src.write_text('x')
        bak_path = backup_file(src)
        # filename pattern: agent.md.bak.<10-or-more-digits>
        self.assertRegex(str(bak_path), r'\.bak\.\d{10,}$')

    def test_two_backups_get_distinct_paths(self):
        src = self.root / 'agent.md'
        src.write_text('x')
        b1 = backup_file(src)
        # ensure timestamp diff (use sub-second precision via time.time_ns)
        b2 = backup_file(src)
        self.assertNotEqual(b1, b2)

    def test_missing_source_raises(self):
        src = self.root / 'nonexistent.md'
        with self.assertRaises(FileNotFoundError):
            backup_file(src)

    def test_returns_string_path(self):
        src = self.root / 'agent.md'
        src.write_text('x')
        bak = backup_file(src)
        self.assertIsInstance(bak, str)


if __name__ == '__main__':
    unittest.main()
