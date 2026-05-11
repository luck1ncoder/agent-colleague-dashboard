import unittest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from cache import file_hash, get_cached, put_cached


class TestCache(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cache_dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_hash_deterministic(self):
        text = "hello world"
        self.assertEqual(file_hash(text), file_hash(text))

    def test_hash_differs_on_change(self):
        self.assertNotEqual(file_hash("a"), file_hash("b"))

    def test_miss_returns_none(self):
        self.assertIsNone(get_cached(self.cache_dir, "abc"))

    def test_round_trip(self):
        put_cached(self.cache_dir, "abc", {"name": "Cole"})
        self.assertEqual(get_cached(self.cache_dir, "abc"), {"name": "Cole"})

    def test_overwrite(self):
        put_cached(self.cache_dir, "abc", {"v": 1})
        put_cached(self.cache_dir, "abc", {"v": 2})
        self.assertEqual(get_cached(self.cache_dir, "abc"), {"v": 2})


if __name__ == '__main__':
    unittest.main()
