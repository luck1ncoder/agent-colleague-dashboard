# Twitter / X Thread Draft · agent-colleague-dashboard

> Use this as a starter. Tweak voice/emoji to match your personality before posting. Each section = one tweet (≤280 chars). Numbering optional — modern threads often drop the "1/" prefix.

---

## Version A — Punchy, hook-first (recommended for first post)

**1/**
You install 6 Claude Code subagents. A week later you can't remember what they do, two of them silently disagree with your CLAUDE.md, and onboarding anyone takes 30 minutes of "let me show you the .md files".

I built a fix. 🧵

**2/**
agent-colleague-dashboard turns your CLAUDE.md and `agents/*.md` into "blogger profile" web pages.

Every agent gets: avatar, MBTI, personality radar, catchphrases, signature moves, daily routine — all inferred from their actual prompt.

Plus a reasoning trace so it's auditable.

[📷 attach social-preview.png]

**3/**
The magic feature: CLAUDE.md ↔ agent **affinity scoring**.

For each agent, the dashboard computes a 0-100 "obedience" score against your CLAUDE.md principles. Low scores get flagged with specific fix suggestions.

> "vibe-coder scored 28 — conflicts with principle 1 (Think Before Coding)"

Your config files surface their own contradictions.

[📷 attach charter.png cropped to affinity section]

**4/**
Edit by talking. Not by hand-editing YAML.

```
/agent-edit code-reviewer "对 magic number 宽容一点"
/claude-edit "add a 5th principle: prefer composition over inheritance"
/agent-create design-reviewer "审 UI 一致性、token 用法、a11y"
```

Backup → diff → you approve → write. Full CRUD via natural language.

**5/**
Tech moat: **zero deps**. Python 3 stdlib only. 105-line template engine. 43 tests. No server, no API key juggling, no `pip install`.

The Edit tool's built-in permission prompt is the diff/confirm UX — we don't reinvent it.

Clone → copy 4 dirs into `~/.claude/skills/` → restart → done.

**6/**
Three layouts auto-pick based on what you have:
- 0 agents → Charter (your CLAUDE.md as a character)
- 1 agent → Focus (full persona page)
- 2+ → Team (CLAUDE.md hero + clickable grid)

[📷 attach team.png]

**7/**
Repo: https://github.com/luck1ncoder/agent-colleague-dashboard

MIT licensed. Stars appreciated. Telling me which feature you'd dogfood first = even more appreciated.

—

What I want to add next:
🔁 cross-project CLAUDE.md comparisons
📌 per-agent edit history + rollback
🎨 exportable "team poster" (one-PNG share)

---

## Version B — Slow-build, problem-first (for second post / different audience)

**1/**
Hot take: configuration files are the most under-designed surface in the AI dev tool space.

Your CLAUDE.md and your subagents are *people* you've hired. But you're stuck reading them as raw markdown like it's 2015 system administration.

**2/**
This week I shipped 4 Claude Code skills that fix this.

The pitch: anthropomorphize your AI team. See them as colleagues. Edit by talking. Let the dashboard tell you when their personalities clash.

[📷 social-preview.png]

**3/**
Each agent gets a full "blogger profile" — Chinese nickname, MBTI inferred from prompt structure, 6-dim personality scores, catchphrases, signature moves, even a daily routine.

It's silly. It works. New people on the team can suddenly tell agents apart in 30 seconds.

[📷 focus-cole.png]

**4/**
The serious bit: **affinity scoring**.

CLAUDE.md is your project's constitution. But the agents you install (or write) may not actually agree with it.

The dashboard computes alignment 0-100 per agent and flags conflicts with specific suggestions. Catches contradictions before they cause bugs.

**5/**
Architecture is boring on purpose:
- Python 3 stdlib only
- 105-line template engine
- Hash-cached LLM inference
- Reuses Edit tool's permission prompt as the diff/confirm UX

Zero external deps. Clone → copy → done.

**6/**
Repo + install in 30 seconds:
https://github.com/luck1ncoder/agent-colleague-dashboard

Built with the @AnthropicAI Claude Code skill system. MIT. Built solo over 7 days of dogfooding.

Would love feedback on what's missing.

---

## Cross-poster bait (for HN / Reddit)

**Title for HN**: `Show HN: Anthropomorphize your Claude Code subagents as blogger profiles`

**HN intro paragraph**:
> This is a bundle of 4 Claude Code skills I wrote to fix a problem I kept hitting: I had ~6 subagents installed across projects, couldn't remember what each did, and twice ran into cases where an installed agent silently disagreed with my project's CLAUDE.md. The dashboard renders each `.md` as a "blogger profile" page with MBTI, personality radar, and catchphrases inferred from the prompt. The unique feature is an affinity scoring step that explicitly flags when an agent's behavior conflicts with CLAUDE.md principles. Zero external dependencies — Python 3 stdlib only, ~30 commits, 43 tests.

**Reddit r/ClaudeAI or r/LocalLLaMA**:
> Title: I anthropomorphized my Claude Code subagents — full repo + skills inside
> (Less formal, more visual. Lead with the social-preview screenshot.)

---

## Posting tips

- **Attach 1280×640 social preview as cover image** on tweet #2 (forces preview card)
- **Don't link the repo in tweet #1** (Twitter algorithm punishes early external links). Save the URL for #7.
- **Quote-tweet @karpathy** thread about LLM coding pitfalls when posting #3 (your CLAUDE.md is derived from his manifesto — citing him is honest + extends reach)
- **Tag @AnthropicAI** in tweet #5 (they sometimes amplify good Claude Code skills)
- **Repost the thread once** ~12 hours later from a different angle (Version B) to catch the other timezone
