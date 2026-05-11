import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from frontmatter import parse


class TestFrontmatter(unittest.TestCase):
    def test_simple(self):
        text = "---\nname: code-reviewer\nmodel: opus\n---\n\nbody here"
        meta, body = parse(text)
        self.assertEqual(meta['name'], 'code-reviewer')
        self.assertEqual(meta['model'], 'opus')
        self.assertEqual(body.strip(), 'body here')

    def test_list_value(self):
        text = "---\ntools: Read, Write, Edit\n---\nbody"
        meta, body = parse(text)
        self.assertEqual(meta['tools'], ['Read', 'Write', 'Edit'])

    def test_quoted_string(self):
        text = '---\ndescription: "use this when X happens"\n---\nbody'
        meta, body = parse(text)
        self.assertEqual(meta['description'], 'use this when X happens')

    def test_no_frontmatter(self):
        text = "no frontmatter here\njust body"
        meta, body = parse(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)

    def test_empty(self):
        meta, body = parse("")
        self.assertEqual(meta, {})
        self.assertEqual(body, "")


if __name__ == '__main__':
    unittest.main()
