"""Minimal YAML frontmatter parser. Supports key: value (string), comma-separated lists,
and double-quoted strings. No nesting, no anchors, no advanced YAML."""
import re

FENCE = '---'


def _parse_value(v):
    v = v.strip()
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    if ',' in v:
        return [item.strip() for item in v.split(',')]
    return v


def parse(text):
    """Parse frontmatter. Returns (metadata_dict, body_str).

    If no frontmatter present, returns ({}, original_text).
    """
    if not text or not text.startswith(FENCE + '\n'):
        return {}, text
    rest = text[len(FENCE) + 1:]
    end = rest.find('\n' + FENCE)
    if end < 0:
        return {}, text
    fm_block = rest[:end]
    body = rest[end + len(FENCE) + 1:]
    if body.startswith('\n'):
        body = body[1:]
    meta = {}
    for line in fm_block.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        meta[key.strip()] = _parse_value(val)
    return meta, body
