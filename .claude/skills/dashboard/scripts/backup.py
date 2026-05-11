#!/usr/bin/env python3
"""Backup a file to <file>.bak.<unix_ns> before modification.

Designed to be cheap: just a copy with a unique-by-time suffix.
Stdlib only.

CLI usage:
  python3 backup.py <file>
  → prints backup path to stdout, returns 0 on success

Module usage:
  from backup import backup_file
  bak_path = backup_file('/path/to/file.md')
"""
import shutil
import sys
import time
from pathlib import Path


def backup_file(src):
    """Copy src to <src>.bak.<timestamp_ns>. Returns backup path as str.

    Raises FileNotFoundError if src does not exist.
    """
    src = Path(src)
    if not src.exists():
        raise FileNotFoundError(f"backup: source not found: {src}")
    suffix = time.time_ns()
    bak = src.with_name(f'{src.name}.bak.{suffix}')
    shutil.copy2(src, bak)
    return str(bak)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: backup.py <file>", file=sys.stderr)
        sys.exit(2)
    print(backup_file(sys.argv[1]))
