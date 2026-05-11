#!/usr/bin/env python3
"""Render persona JSON + HTML template → output HTML.

Usage:
  python3 render.py --json data.json --template tmpl.html --out output.html
"""
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from tmpl_engine import render


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', required=True, help='persona JSON path')
    ap.add_argument('--template', required=True, help='HTML template path')
    ap.add_argument('--out', required=True, help='output HTML path')
    args = ap.parse_args()

    data = json.loads(Path(args.json).read_text(encoding='utf-8'))
    template = Path(args.template).read_text(encoding='utf-8')
    output = render(template, data)
    Path(args.out).write_text(output, encoding='utf-8')
    print(f"wrote {args.out}", file=sys.stderr)


if __name__ == '__main__':
    main()
