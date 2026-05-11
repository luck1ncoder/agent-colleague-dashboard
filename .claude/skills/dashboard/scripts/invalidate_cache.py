#!/usr/bin/env python3
"""Delete the dashboard persona-cache entry for a given .md source file.

The cache key is the SHA256-hex (16 chars) of the file's text content. After
an edit, the old key's entry is stale — remove it so /dashboard re-infers next
time.

CLI usage:
  python3 invalidate_cache.py <md_path> [<cache_dir>]
  → prints the number of files removed

Module usage:
  from invalidate_cache import invalidate
  n = invalidate(md_path, cache_dir='~/.claude/dashboard-cache')
"""
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from cache import file_hash


def invalidate(md_path, cache_dir):
    """Remove cached JSON and HTML for the given .md path.

    Returns the number of files removed (0, 1, or 2). If md_path doesn't exist,
    returns 0 silently (file was deleted; nothing to invalidate against).

    IMPORTANT: must be called BEFORE the .md file is modified (while it still
    contains the content that produced the cache key). Calling after a write
    will compute a different hash and never find the stale entry.
    """
    md_path = Path(md_path)
    cache_dir = Path(cache_dir)
    if not md_path.exists():
        return 0
    text = md_path.read_text(encoding='utf-8')
    h = file_hash(text)
    removed = 0
    json_target = cache_dir / f'{h}.json'
    if json_target.exists():
        json_target.unlink()
        removed += 1
    html_target = cache_dir / f'{h}.html'
    if html_target.exists():
        html_target.unlink()
        removed += 1
    return removed


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: invalidate_cache.py <md_path> [<cache_dir>]", file=sys.stderr)
        sys.exit(2)
    md_path = sys.argv[1]
    cache_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/.claude/dashboard-cache')
    n = invalidate(md_path, cache_dir)
    print(n)
