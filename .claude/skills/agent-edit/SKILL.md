---
name: agent-edit
description: Modify an existing agent's `.claude/agents/<name>.md` file based on a natural-language request. Triggered by /agent-edit. Backs up the file, uses the Edit tool (which prompts the user with a diff for permission), and invalidates the dashboard cache. Use when the user wants to change an agent's behavior, prompt, tools, or model without manually editing the file.
---

# agent-edit skill

Modify an existing agent's prompt file based on natural-language instructions. The user describes the change; you (the LLM) figure out where in the file to apply it and use the Edit tool to make the change. The user reviews the diff via the Edit tool's built-in permission prompt.

## Trigger

```
/agent-edit <agent-name> "<natural-language change request>"
```

Examples:
- `/agent-edit code-reviewer "对 magic number 宽容一点"`
- `/agent-edit vibe-coder "add a When invoked step about reading existing tests first"`
- `/agent-edit planner "switch model from sonnet to opus"`

## Pipeline

### Step A. Resolve the agent file

Search in this order, take first match:
1. `.claude/agents/<name>.md` (project-level)
2. `~/.claude/agents/<name>.md` (user-level)

If not found:
- Tell the user the agent doesn't exist
- List available agents (project + user dirs combined, deduplicated by stem name)
- Suggest `/agent-create <name>` if they wanted to make a new one (note: that command is part of a future plan and may not exist yet)
- Stop. Do not create new files in this skill.

### Step B. Read the current file

Use the Read tool on the resolved path. Note frontmatter fields and body sections.

### Step C. Plan the change

Translate the natural-language request into a targeted edit. Be specific:
- If the user says "对 magic number 宽容一点", the target is the line(s) about magic numbers — soften wording (e.g., "magic number 拒绝" → "magic number 警告但不阻止"), don't rewrite unrelated parts.
- If the user says "add a When invoked step", append one numbered item to the existing list.
- If the user says "switch model", change only the `model:` value in frontmatter.

**Hard rules:**
- Modify ONLY the resolved file. Never touch other agent files or CLAUDE.md from this skill.
- Make the smallest change that satisfies the request. Don't refactor or "improve" surrounding content.
- Preserve formatting (heading levels, list style, indentation, spacing).
- If the request is genuinely ambiguous, ASK the user before editing — don't guess.

### Step D. Backup before edit

Run via Bash:
```
DASHBOARD=.claude/skills/dashboard
python3 $DASHBOARD/scripts/backup.py <resolved-path>
```

The backup path will print to stdout. Note it for the report.

### Step E. Invalidate the dashboard cache (before the edit)

Run via Bash:
```
python3 $DASHBOARD/scripts/invalidate_cache.py <resolved-path>
```

This MUST happen before the Edit (while the file still has its pre-edit content). Calling after the edit hashes the new content and finds nothing to remove, leaving stale entries in `~/.claude/dashboard-cache/`.

### Step F. Apply the edit

Use the Edit tool. The Edit tool will:
1. Display the proposed change as a diff
2. Ask the user for permission to apply
3. Apply only on user approval

If the user rejects the edit, stop. The backup file is left in place (it's harmless, gitignored, and can be cleaned up manually if desired).

### Step G. Report back

Tell the user, in one short message:
1. What was changed (one sentence)
2. Backup location (so they can rollback)
3. Suggest re-running the dashboard to see the new persona

Example:
> 已把 code-reviewer 对 magic number 的态度从"拒绝"改为"警告但不阻止"。
> 备份: `~/.claude/agents/code-reviewer.md.bak.1714823104938293000`
> 想看新版人设：`/dashboard --agent code-reviewer`

## Safety boundaries

- **Single-file scope.** This skill modifies exactly one file per invocation. Never edit other agent files, CLAUDE.md, or anything outside `.claude/agents/` (project) or `~/.claude/agents/` (user).
- **Backup is mandatory.** Always call `backup.py` before the Edit tool. Even if the user requested a tiny change.
- **No silent destruction.** If the user's request implies removing a large section, ask first ("This will remove the entire 'Code review checklist' block — confirm?").
- **No frontmatter corruption.** When editing frontmatter, preserve `---` delimiters and YAML syntax. If you must change the `name` field, warn the user that this will rename the file effectively.
- **Don't add new files.** This skill only modifies existing agents. Creating new agents is out of scope.
- **No affinity warning here.** Agent edits don't change CLAUDE.md → agent affinity scoring is driven by CLAUDE.md content, not agent prompts. (`/claude-edit` does emit such a warning.)
