import unittest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from invalidate_cache import invalidate
from cache import put_cached


class TestInvalidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cache_dir = Path(self.tmp.name)
        self.src = self.cache_dir / 'src.md'
        self.src.write_text('hello world')

    def tearDown(self):
        self.tmp.cleanup()

    def test_removes_existing_cache_entry(self):
        from cache import file_hash
        h = file_hash(self.src.read_text())
        put_cached(self.cache_dir, h, {"name": "x"})
        # Confirm cache exists
        self.assertTrue((self.cache_dir / f'{h}.json').exists())
        n = invalidate(self.src, self.cache_dir)
        self.assertEqual(n, 1)
        self.assertFalse((self.cache_dir / f'{h}.json').exists())

    def test_removes_paired_html_file(self):
        from cache import file_hash
        h = file_hash(self.src.read_text())
        # Create both .json and .html cache entries
        put_cached(self.cache_dir, h, {"name": "x"})
        (self.cache_dir / f'{h}.html').write_text('<html>cached</html>')
        n = invalidate(self.src, self.cache_dir)
        self.assertEqual(n, 2)
        self.assertFalse((self.cache_dir / f'{h}.json').exists())
        self.assertFalse((self.cache_dir / f'{h}.html').exists())

    def test_no_cache_entry_returns_zero(self):
        n = invalidate(self.src, self.cache_dir)
        self.assertEqual(n, 0)

    def test_missing_source_returns_zero(self):
        # If source doesn't exist, just no-op (the .md was deleted; whatever)
        nonex = self.cache_dir / 'nope.md'
        n = invalidate(nonex, self.cache_dir)
        self.assertEqual(n, 0)


if __name__ == '__main__':
    unittest.main()
