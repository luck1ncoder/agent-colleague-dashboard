---
name: claude-edit
description: Modify the project's `CLAUDE.md` (or `~/.claude/CLAUDE.md` user-level) based on a natural-language request. Triggered by /claude-edit. Backs up the file, uses the Edit tool (with built-in diff and permission prompt), and invalidates the dashboard cache. Use when the user wants to change the project charter — adding, removing, or rewording principles, rules, or constraints.
---

# claude-edit skill

Modify the project's CLAUDE.md based on natural-language instructions. Same pattern as `agent-edit` but targeting the charter file instead of an agent file.

## Trigger

```
/claude-edit "<natural-language change request>"
```

Examples:
- `/claude-edit "add a 5th principle: prefer composition over inheritance"`
- `/claude-edit "remove the 'No mocking' rule — we agreed it's too strict"`
- `/claude-edit "soften principle 3 to allow refactoring when explicitly asked"`

## Pipeline

### Step A. Resolve CLAUDE.md

Search in this order, take first match:
1. `./CLAUDE.md` (project root)
2. `~/.claude/CLAUDE.md` (user-level)

If neither exists:
- Tell the user "no CLAUDE.md found in project root or ~/.claude/"
- Ask if they want to create one (note: this skill does not create new files; suggest manual creation or a future `/claude-create` command)
- Stop.

### Step B. Read the file

Use the Read tool on the resolved path. Take note of:
- Top-level structure (`# CLAUDE.md`, `## 1. ...`, etc.)
- Style (bullet points vs prose, heading depth, numbering scheme)
- Any explicit "## Principles" or numbered sections

### Step C. Plan the change

Translate the request into a precise edit:
- "Add a 5th principle" → append a new `## 5. <Title>` section after the last principle, matching style
- "Remove rule X" → delete just that section, leaving surrounding sections intact
- "Soften principle 3" → reword the text inside section 3 only

**Hard rules:**
- Modify ONLY `CLAUDE.md`. Never touch agent files from this skill.
- Match existing heading depth, numbering, and prose style.
- Preserve any sections the request didn't ask to change.
- If unclear ("rewrite section X" without saying how), ASK before editing.

### Step D. Backup before edit

```
DASHBOARD=.claude/skills/dashboard
python3 $DASHBOARD/scripts/backup.py <resolved-path>
```

### Step E. Invalidate the dashboard cache (before the edit)

Run via Bash:
```
python3 $DASHBOARD/scripts/invalidate_cache.py <resolved-path>
```

This MUST happen before the Edit (while the file still has its pre-edit content). Calling after the edit hashes the new content and finds nothing to remove, leaving stale entries in `~/.claude/dashboard-cache/`.

### Step F. Apply the edit

Use the Edit tool. The diff is shown to the user; they approve or reject.

### Step G. Affinity recompute warning

If the project has agents (`.claude/agents/*.md` exists), remind the user that the CLAUDE.md change may invalidate previously-computed affinity scores. Suggest re-running `/dashboard` (default mode) to see updated alignment.

### Step H. Report back

Tell the user:
1. What was changed (one sentence)
2. Backup path
3. Suggest `/dashboard --claude` (or `/dashboard` to see team affinity recomputed)

Example:
> 已在 CLAUDE.md 末尾加了原则 5: "组合优于继承"。
> 备份: `./CLAUDE.md.bak.1714823104938293000`
> 想看团队对新原则的服从度：`/dashboard`

## Safety boundaries

- **Single-file scope.** Only modifies the resolved CLAUDE.md.
- **Backup mandatory.** Always before Edit.
- **Preserve unmodified sections.** If user asks to change one principle, leave the others alone.
- **No silent destruction.** If the request implies removing a major section, confirm first.
- **Don't auto-fix downstream agents.** If the new CLAUDE.md conflicts with an existing agent, mention it but don't edit the agent — that's a separate `/agent-edit` invocation.
