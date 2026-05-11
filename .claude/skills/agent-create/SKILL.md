---
name: agent-create
description: Create a new subagent at `.claude/agents/<name>.md` from a natural-language description. Triggered by /agent-create. Reads CLAUDE.md to inherit project style/constraints, drafts a properly-formatted agent.md, uses the Write tool (which prompts the user with the full content for permission), and tells the user how to view the new agent. Use when the user wants a new agent and doesn't want to hand-write the .md frontmatter and prompt.
---

# agent-create skill

Create a brand-new subagent file from a natural-language description. The user names the agent and describes what it should do; you (the LLM) draft the `.md`, propose it via the Write tool, and the user approves.

This completes the CRUD triad alongside `/dashboard` (read), `/agent-edit` (update), and is the recommended Create path instead of Claude Code's interactive `/agents` wizard for users who already know what they want.

## Trigger

```
/agent-create <name> "<natural-language description>"
```

Examples:
- `/agent-create design-reviewer "审 UI 一致性、组件 token 用法、a11y 基础"`
- `/agent-create db-migrator "draft + review database migrations, never destructive"`
- `/agent-create release-notes "summarize git diffs into release notes for non-engineers"`

## Pipeline

### Step A. Validate the name

The `<name>` arg must be a kebab-case identifier (lowercase letters, digits, hyphens). Reject names with spaces, uppercase, slashes, or special chars — tell the user the rule and stop.

Check that no agent with this name already exists:
- `.claude/agents/<name>.md`
- `~/.claude/agents/<name>.md`

If either exists: tell the user that agent already exists, suggest `/agent-edit <name> "..."` to modify it, and stop. Do NOT silently overwrite.

### Step B. Pick the destination

Default to project-level: `.claude/agents/<name>.md`.

Only put the agent at `~/.claude/agents/<name>.md` if the user explicitly says "user-level" or "global" in their description. Otherwise project-level is correct (most agents should live with the project that defines their context).

### Step C. Read CLAUDE.md to inherit project style

Find CLAUDE.md (project then user). If it exists, read it and note:
- Tone (terse manifesto vs. verbose? casual vs. formal?)
- Hard rules / aversions (so the new agent doesn't violate them)
- Existing structural patterns (numbered principles? heading style?)

If no CLAUDE.md, just use defaults.

### Step D. Draft the agent .md

Compose the file with this structure (be CRITICAL of your own draft — see `## Hard rules` below):

```markdown
---
name: <kebab-case-name>
description: <one-line description starting with "Use this agent when..." or similar trigger phrase>
tools: <minimal toolset — see "Tool selection" below>
model: <opus | sonnet | haiku — see "Model selection" below>
---

You are a <role> with expertise in <domain>. <One-line positioning that reflects the user's description.>

When invoked:
1. <Step from user's description>
2. <Step>
3. <Step>
4. <Provide actionable feedback / ship the artifact>

<Optional: a domain-specific checklist or anti-pattern list that's actually load-bearing for this agent. NOT a copy-paste of generic best practices.>
```

**Tool selection** (right-size, don't grab everything):
- Read-only inspector (reviewer, auditor, analyzer) → `Read, Glob, Grep`
- Editor / refactor → `Read, Edit, Glob, Grep` (no Write — Edit covers both)
- Build something new → `Read, Write, Edit, Bash, Glob, Grep`
- Net access required → add `WebFetch, WebSearch`

**Model selection**:
- Routine, mechanical, single-domain → `haiku`
- Standard implementation, code review, judgment calls → `sonnet`
- Architecture, multi-file refactor, deep reasoning → `opus`

Default: `sonnet` if unsure.

### Step E. Cross-check against CLAUDE.md

Before proposing the file: re-read CLAUDE.md and check that your draft doesn't violate any of its principles. If there's a tension (e.g., CLAUDE.md says "never auto-format" but your agent's bio says "auto-formats files"), flag it explicitly to the user — don't bury it.

### Step F. Propose the file via the Write tool

Use the Write tool with the resolved path. Claude Code will:
1. Show the user the full proposed content
2. Ask for permission to write
3. Create the file only on user approval

If the user rejects, stop. Do not retry without new instructions.

### Step G. Report back

Tell the user, in one short message:
1. The new agent's name + role + tier (one sentence)
2. Where the file landed (project or user dir)
3. How to see it: `/dashboard --agent <name>` to view its full persona; `/dashboard` to see it in the team grid
4. How to refine: `/agent-edit <name> "..."` for any tweaks

Example:
> 已创建 design-reviewer (Sonnet 级 · UI 审查师) → `.claude/agents/design-reviewer.md`
> 看人设: `/dashboard --agent design-reviewer`
> 想改: `/agent-edit design-reviewer "..."`

## Hard rules

- **Never overwrite an existing agent.** If the file exists, refuse and route the user to `/agent-edit`.
- **Never write outside `.claude/agents/` or `~/.claude/agents/`.** Anything else is out of scope.
- **Frontmatter is mandatory** with at least `name`, `description`, `tools`, `model`. No skipping fields.
- **No fake confidence.** If the user's description is too vague to draft a focused agent (e.g., "make a helper agent"), ASK what specifically it should do — don't guess.
- **Don't pad the body.** A 50-line agent is better than a 200-line agent. Karpathy's CLAUDE.md is 50 lines and it's the load-bearing one in this project. Be concise.
- **No CLAUDE.md violations.** Cross-check before proposing.
- **No "best-of" naming gimmicks.** The name should describe what the agent DOES, not be cute. `code-reviewer` ✓ , `super-genius-coder-9000` ✗.
