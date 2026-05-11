"""Tiny template engine: {{var}}, {{var.path}}, {{#each list}}...{{/each}}, {{#if var}}...{{/if}}.

Supports nested {{#each}} and {{#if}} blocks. Stdlib only.
"""
import re

VAR_RE = re.compile(r'\{\{\s*([^{}#/][^{}]*?)\s*\}\}')
BLOCK_OPEN_RE = re.compile(r'\{\{#(each|if)\s+(\S+?)\s*\}\}')
BLOCK_CLOSE_RE = re.compile(r'\{\{/(each|if)\}\}')


def _resolve(path, data):
    cur = data
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _truthy(v):
    if v is None: return False
    if v is False: return False
    if v == 0: return False
    if v == '': return False
    if isinstance(v, (list, dict)) and len(v) == 0: return False
    return True


def _split_blocks(template):
    """Split template into a list of segments: strings and block dicts.

    A block dict has keys: type ('each'|'if'), path, body (str).
    Handles arbitrary nesting.
    """
    result = []
    pos = 0
    while pos < len(template):
        open_m = BLOCK_OPEN_RE.search(template, pos)
        if not open_m:
            result.append(template[pos:])
            break
        # text before block
        if open_m.start() > pos:
            result.append(template[pos:open_m.start()])
        block_type = open_m.group(1)
        block_path = open_m.group(2)
        # find matching close, respecting nesting
        depth = 1
        scan = open_m.end()
        while depth > 0 and scan < len(template):
            next_open = BLOCK_OPEN_RE.search(template, scan)
            next_close = BLOCK_CLOSE_RE.search(template, scan)
            if not next_close:
                # malformed — treat rest as literal
                scan = len(template)
                break
            if next_open and next_open.start() < next_close.start():
                depth += 1
                scan = next_open.end()
            else:
                depth -= 1
                if depth == 0:
                    body = template[open_m.end():next_close.start()]
                    result.append({'type': block_type, 'path': block_path, 'body': body})
                    pos = next_close.end()
                    break
                scan = next_close.end()
        else:
            pos = scan
    return result


def _render(template, data):
    segments = _split_blocks(template)
    parts = []
    for seg in segments:
        if isinstance(seg, str):
            # render variables in plain text
            def sub(m, data=data):
                v = _resolve(m.group(1), data)
                return '' if v is None else str(v)
            parts.append(VAR_RE.sub(sub, seg))
        else:
            block_type = seg['type']
            path = seg['path']
            body = seg['body']
            if block_type == 'each':
                items = _resolve(path, data)
                if isinstance(items, list):
                    for item in items:
                        local = dict(data)
                        local['this'] = item
                        parts.append(_render(body, local))
            elif block_type == 'if':
                val = _resolve(path, data)
                if _truthy(val):
                    parts.append(_render(body, data))
    return ''.join(parts)


def render(template, data):
    """Render template string with data dict."""
    return _render(template, data)
