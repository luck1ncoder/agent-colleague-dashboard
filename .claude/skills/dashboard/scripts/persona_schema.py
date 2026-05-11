"""Canonical persona JSON shape — for documentation and test fixtures.

Not enforced (no jsonschema dep). Use as reference when LLM emits JSON.
"""

PERSONA_KEYS = {
    'type': 'agent | claude_md',
    'source_path': 'absolute path to .md file',
    'name': 'frontmatter name (e.g. code-reviewer)',
    'cn_name': '2-3 char Chinese花名',
    'avatar_emoji': 'one emoji',
    'model': 'opus | sonnet | haiku',
    'tier': 'S | A | B (derived from model)',
    'tools': 'list[str]',
    'title_line': 'one line role',
    'bio': 'first-person 1-2 sentence intro',
    'mbti': '4-letter code',
    'mbti_name': 'Chinese 人格名',
    'archetype': 'one phrase positioning',
    'tags': 'list[str] of 6-8 hashtags (with #)',
    'personality': 'dict with 6 numeric scores 0-100',
    'basic': 'dict with gender/birthday/blood_type/education/origin/joined',
    'quotes': 'list[str]',
    'moves': 'list[{icon, name, desc}]',
    'peeves': 'list[str]',
    'daily': 'list[{time, do}]',
    'playlist': 'list[{title, artist}]',
    'books': 'list[{label, title}]',
    'coop': 'dict with good/warn/bad arrays of agent names',
    'reviews': 'list[{stars, text, reviewer}]',
    'stats': 'dict with monthly_calls/p0_caught/prs_reviewed/last_seen',
    'reasoning_trace': 'list[{conclusion, sources, reasoning}]',
}

TIER_FROM_MODEL = {'opus': 'S', 'sonnet': 'A', 'haiku': 'B'}
