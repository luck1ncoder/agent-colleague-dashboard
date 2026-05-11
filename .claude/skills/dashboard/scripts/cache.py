"""Hash-based JSON cache for inferred persona data.

The hash is over the .md file's text content; same content → same persona, no re-inference needed.
"""
import hashlib
import json
from pathlib import Path


def file_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def get_cached(cache_dir, key):
    p = Path(cache_dir) / f'{key}.json'
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def put_cached(cache_dir, key, obj):
    p = Path(cache_dir)
    p.mkdir(parents=True, exist_ok=True)
    (p / f'{key}.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
