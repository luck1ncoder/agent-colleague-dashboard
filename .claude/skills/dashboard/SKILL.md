---
name: dashboard
description: Render agent.md and CLAUDE.md as anthropomorphized HTML profiles. Triggered by /dashboard. Auto-detects layout (Focus for single agent, Team for multiple, CLAUDE.md-only when no agents). Use when user asks to visualize, view, or explain their Claude Code agents and project charter.
---

# Dashboard skill

Visualize Claude Code's `CLAUDE.md` and `agents/*.md` as "blogger profile"-style HTML pages.

## Trigger

User types `/dashboard` (default) or with explicit args:
- `/dashboard --agent <name>` → Focus mode for one agent
- `/dashboard --team` → Team mode (CLAUDE.md hero + agent grid)
- `/dashboard --claude` → CLAUDE.md-only mode

## Pipeline (overall)

1. Determine mode (auto or from args)
2. For each .md file in scope: read, infer persona JSON, cache
3. Render the appropriate template with the JSON
4. `open` the HTML in browser

## File layout

- `scripts/render.py` — JSON + template → HTML
- `scripts/detect_mode.py` — pick mode from agent count
- `scripts/frontmatter.py` — parse YAML frontmatter
- `scripts/cache.py` — hash-based JSON cache
- `templates/agent-profile.html` — Focus mode
- `templates/team-dashboard.html` — Team mode (Task 13)
- `templates/claude-charter.html` — CLAUDE.md mode (Task 14)
- `samples/*.json` — canonical examples for testing

## Mode: Focus (`/dashboard --agent <name>`)

When the user asks to view a specific agent:

### Step A. Locate the agent file

Search in this order, take first match:
1. `.claude/agents/<name>.md` (project-level)
2. `~/.claude/agents/<name>.md` (user-level)

If not found: tell the user the agent doesn't exist and list available agent names from the search dirs.

### Step B. Check cache

Compute `file_hash(file_text)`. If `~/.claude/dashboard-cache/<hash>.json` exists, load it; skip to Step D.

### Step C. Infer persona JSON

Read the file. Parse frontmatter and body. Output a JSON object matching this shape (every field must be present):

```jsonc
{
  "type": "agent",
  "source_path": "<absolute path to .md>",
  "name": "<from frontmatter>",
  "cn_name": "<2-3 char Chinese花名 you choose, evoking the role>",
  "avatar_emoji": "<one emoji that captures the agent's vibe>",
  "model": "<from frontmatter>",
  "tier": "<S=opus, A=sonnet, B=haiku>",
  "tools": ["<from frontmatter>"],
  "title_line": "<one line role description, e.g. '资深代码审查师 · Quality 部 · 入职 N 年'>",
  "bio": "<first-person 1-2 sentence intro from agent's perspective>",
  "mbti": "<4-letter code inferred from prompt's structural traits>",
  "mbti_name": "<Chinese 人格名 e.g. 检察官>",
  "archetype": "<one phrase, e.g. '完美主义晚期'>",
  "tags": ["<6-8 hashtag tags including MBTI, zodiac, vibe>"],
  "personality": {
    "rigor": <0-100>, "speed": <0-100>, "empathy": <0-100>,
    "creative": <0-100>, "stress": <0-100>, "communication": <0-100>
  },
  "basic": {
    "gender": "<inclusive default like they/them>",
    "birthday": "<random plausible date matching MBTI archetype with zodiac sign emoji>",
    "blood_type": "<A/B/O/AB type with one-line stereotype>",
    "education": "<thematic joke degree, e.g. 'SICP 重读 7 遍'>",
    "origin": "<github org or playful birthplace>",
    "joined": "<plausible date>",
    "team": "<short team name e.g. 'Quality 部'>",
    "location": "<short path display, e.g. '~/.claude/agents/'>"
  },
  "quotes": ["<4-5 catchphrases inferred from prompt's voice>"],
  "moves": [{"icon": "<emoji>", "name": "<招式名>", "desc": "<short desc>"}],
  "peeves": ["<5 things this agent finds intolerable, derived from prompt's anti-patterns>"],
  "daily": [{"time": "<HH:MM>", "do": "<activity inferred from When invoked steps>"}],
  "playlist": [{"num": "01", "title": "<song matching agent's vibe>", "artist": "<artist>"}],
  "books": [{"label": "<emoji + label>", "title": "<book matching domain>"}],
  "coop": {"good": ["<other agent names>"], "warn": [], "bad": []},
  "reviews": [{"stars": <1-5>, "stars_str": "<★★★★★ matching count>", "text": "<faux quote>", "reviewer": "<name>"}],
  "stats": {
    "monthly_calls": <plausible 10-100>,
    "p0_caught": <plausible 0-10>,
    "prs_reviewed": <plausible 0-200>,
    "last_seen": "<ISO 8601>",
    "last_seen_pretty": "<human-readable last action>"
  },
  "reasoning_trace": [
    {
      "conclusion": "<what was inferred>",
      "sources": ["<exact prompt snippet that supports it>", "..."],
      "reasoning": "<one-line explanation of the leap>"
    }
  ]
}
```

**Inference rules:**
- The same .md should always produce the same JSON. Use the file content as the only source of truth — do not invent traits not implied by the prompt.
- **Reasoning trace is mandatory** — at minimum 4 entries (MBTI, two personality scores with extreme values, one peeve mapping). Each entry's sources must be verbatim quotes from the prompt.
- For `coop`, only list other agents that exist in the same project (you can read sibling .md files to know names). If you don't know, leave arrays empty.

**Every rendered Focus / CLAUDE.md page must include a `source_text` field** containing the raw .md content, HTML-escaped (`&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`). The template renders it inside a collapsible `<details><pre>` block at the bottom so the user can verify the persona against the original. Also include `source_lines` (integer line count). Team mode pages do NOT need source_text (the source for each agent lives on its own Focus page).

**Every rendered page (Focus / Team / CLAUDE.md) must include a `nav` block** so the topnav renders cross-page links. Compose it once, inject into every JSON before render:

```jsonc
"nav": {
  "project_name": "<project dir basename>",
  "charter_url": "file://<absolute>/charter-<hash>.html",
  "team_url": "file://<absolute>/team-<hash>.html",
  "agents": [
    {"name": "code-reviewer", "cn_name": "柯瑞", "avatar_emoji": "🧐",
     "url": "file://<absolute>/<agent-hash>.html"}
  ],
  "no_agents": false
}
```

For CLAUDE.md mode when 0 agents exist: set `nav.no_agents: true` and `nav.agents: []` — the charter template will render an empty-state CTA inviting the user to run `/agents`.

### Step D. Save to cache, render, open

1. Write JSON to `~/.claude/dashboard-cache/<hash>.json` via Bash.
2. Run `python3 .claude/skills/dashboard/scripts/render.py --json <cache>.json --template .claude/skills/dashboard/templates/agent-profile.html --out ~/.claude/dashboard-cache/<hash>.html` via Bash.
3. Run `open ~/.claude/dashboard-cache/<hash>.html` to launch browser.
4. Tell the user the file path and a one-line summary ("Rendered 柯瑞 · Focus mode → opening browser").

## Mode: Team (`/dashboard --team` or auto when 2+ agents)

### Step A. Discover all agents

Use `scan_agents()` from `scripts/detect_mode.py` (or replicate logic): list `*.md` from `.claude/agents/` then `~/.claude/agents/`, dedup by stem name, project takes precedence.

### Step B. Read CLAUDE.md

Find CLAUDE.md in this order:
1. `./CLAUDE.md` (project root)
2. `~/.claude/CLAUDE.md`

If neither exists: skip the CLAUDE.md hero, render a placeholder ("项目暂无宪章").

### Step C. For each agent, also pre-render its Focus page

For each agent, run the full Focus pipeline (Steps A-D from the Focus mode section) so its detail page exists in cache. Note the resulting hash for each.

This makes mini-cards in the team page clickable — they link straight to the Focus HTML.

### Step D. For each agent, infer mini-persona (with focus_url)

Output a compact JSON for the team grid (just the fields used in mini-card — see `samples/team.json` for shape). Skip the full reasoning_trace and big arrays. **Each agent must include `focus_url`**: `file:///<absolute-path-to-focus-html-in-cache>` (use `~` expansion to the absolute home dir).

### Step E. Compose team JSON

Merge the CLAUDE.md persona, agent mini-personas, and computed stats (`online_pretty`, `tier_distribution`) into one team JSON.

### Step F. Render + open

Use `templates/team-dashboard.html`. Same render-and-open pattern as Focus mode.

The rendered team HTML wraps each mini-card in `<a href="{{focus_url}}">` — clicking a card opens that agent's Focus page in the same browser tab.

## Mode: CLAUDE.md (`/dashboard --claude` or auto when 0 agents)

### Step A. Find CLAUDE.md

Search order: `./CLAUDE.md`, `~/.claude/CLAUDE.md`. If neither: tell user "no CLAUDE.md found in project or user dir" and exit.

### Step B. Infer charter persona

Output JSON matching `samples/claude-md.json` shape. Same inference principles as agent persona — but treat the document as the entity:
- `cn_title`: name the charter ("约法四章" / "守则" — your call based on tone)
- `vibe`: one phrase capturing the document's character
- `mbti`: yes, CLAUDE.md has an MBTI too (e.g., ISTJ-J for rule-heavy charters, ENFP for permissive ones)
- `principles`: extract the top-level principles from the doc body
- `aversions`: list things the doc forbids/discourages
- `origin_story`: one paragraph on where the doc came from (Karpathy风/项目原创/OSS模板)
- `personality`: 6 numeric scores (rigor, speed, empathy, creative, stress, communication)

### Step C. Compute affinity (CLAUDE.md ↔ each agent)

For each agent in `.claude/agents/` and `~/.claude/agents/`:
1. Read the agent's prompt
2. Score 0-100 on how well the agent's behavior aligns with each CLAUDE.md principle
3. Average the per-principle scores → affinity score
4. Set `level`: `high` if ≥75, `mid` if 50-74, `low` if <50

If any agent's score < 50, set `has_low_affinity: true` and write a `low_affinity_warning` explaining the specific conflict and proposing a fix.

### Step D. Render + open

Use `templates/claude-charter.html`. Same pattern.
## Smart default (`/dashboard` with no args)

### Step A. Scan agents

Run via Bash:
```
python3 .claude/skills/dashboard/scripts/detect_mode.py 2>&1 || true
```

Or replicate the logic inline: count agents in `.claude/agents/*.md` ∪ `~/.claude/agents/*.md` (dedupe by name).

### Step B. Pick mode

- 0 agents → CLAUDE.md mode (Step A of CLAUDE.md section)
- 1 agent → Focus mode (Step A of Focus section, with that single agent name)
- 2+ agents → Team mode (Step A of Team section)

### Step C. Execute the chosen mode

Follow that mode's pipeline.

### Step D. Tell the user what was rendered

One line: "Detected N agents → rendered Team mode → opening browser." Include the file path so the user can re-open if needed.
