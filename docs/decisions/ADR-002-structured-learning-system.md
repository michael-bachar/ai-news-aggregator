---
id: ADR-002
date: 2026-03-22
status: accepted
supersedes: ~
---

# Build a structured learning system alongside the codebase

## Context
Building with AI across many sessions creates a compounding problem: each session starts blank. Without a deliberate system, the same mistakes get made twice, architectural reasoning gets lost, and mental models don't carry forward. The goal is not just to ship a working product but to get better at building with AI over time.

## Options considered
- **No system** — rely on git history and CLAUDE.md. Simple, but git history captures what changed, not why. CLAUDE.md gets bloated if it absorbs everything.
- **Single lessons file** — one `tasks/lessons.md` for everything. Better than nothing, but conflates project-specific mistakes with architectural decisions with personal growth.
- **Structured multi-file system** — separate files for separate purposes. More folders, but each one has a clear job and a clear audience.

## Decision
Maintain four distinct knowledge stores, each with a different purpose:

| File/Folder | Purpose |
|---|---|
| `tasks/lessons.md` | Project-specific lessons — bugs, patterns, rules |
| `docs/decisions/` | Architecture Decision Records — why X over Y |
| `docs/learnings/` | Meta lessons about building with AI — process insights, LinkedIn content |
| `docs/brainstorms/` | Pre-build reasoning — what was considered before building |

CLAUDE.md loads all of these at session startup via explicit read instructions, so they're applied automatically without needing to be re-explained.

## Consequences
- Future sessions start with full context on decisions, mistakes, and mental models
- Architectural decisions don't get re-litigated — the reasoning is on record
- Personal growth as an AI builder is tracked separately from project state
- Requires a "let's compound" ritual at the end of sessions to stay populated
- If the ritual breaks down, the files go stale and the system loses value
