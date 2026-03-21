# AI News Aggregator — CLAUDE.md

## How This System Works
See @docs/system-guide.md for a full explanation of the file structure, build process, and how to use PRPs.

**Before any feature work:** Read @docs/brainstorms/ for relevant prior decisions. The brainstorm doc captures all key architecture, stack, and scope decisions made before implementation began.

## Model Selection
- **Opus** — complex, multi-phase builds, architecture decisions, anything touching 5+ files
- **Sonnet** — simple tasks, single-file edits, quick fixes

## Plan Mode (use this, every session)
Press **Shift+Tab twice** to activate. Claude reads files and writes a plan without touching any code.
Press **Ctrl+G** to open the plan in your editor and annotate it before executing.
Exit plan mode and Claude one-shots the implementation from the approved plan.

## Build Loop (the mental model)
**Simple task** (describable in one sentence) → just do it directly
**Medium task** (multi-file, clear scope) → Plan Mode → execute
**Complex feature** (multi-phase, architecture decisions) → brainstorm → INITIAL.md → /generate-prp → /execute-prp

For complex features:
- UNDERSTAND: /research before writing INITIAL.md
- SPECIFY: fill INITIAL.md → /generate-prp → produces PRP
- ALIGN: annotate PRP inline → "address notes, don't implement yet" → iterate
- BUILD: /execute-prp → Ralph loop (implement → validate → fix → validate → proceed)
- VERIFY: /review-phase in fresh context (Writer/Reviewer pattern)
- COMPOUND: update tasks/lessons.md + examples/ + CLAUDE.md (explicit, every phase)

## Project
Agentic AI news aggregator — pulls from RSS feeds, newsletters, and email to surface what's worth reading.
Filters signal from noise, synthesizes key developments, and delivers a ranked digest on a schedule.

**V1:** RSS + YouTube transcript ingestion → Jaccard deduplication → Claude scoring → Claude clustering → Claude synthesis → web dashboard (daily + weekly views)
**V2:** Multi-user, hosted, LinkedIn content generation handoff to Content Agent

**Agents:** Python, Claude API (Anthropic SDK)
**Storage:** SQLite
**Delivery:** FastAPI + Jinja2 web dashboard
**Scheduler:** GitHub Actions (6am daily, Sunday weekly)
**Config:** All user-specific data in config.yaml — sources, topics, relevance criteria. Nothing hardcoded.

---

## Architecture
```
ai-news-aggregator/
├── src/
│   ├── ingestion/       # RSS, newsletter, and email readers
│   ├── scoring/         # Relevance scoring agent
│   ├── synthesis/       # Summarization and digest generation agent
│   ├── delivery/        # Output formatters (CLI, email, Slack)
│   └── storage/         # DB models and queries
├── evals/               # Evaluation scripts for scoring and summaries
├── examples/            # Sample inputs/outputs for agent context
├── PRPs/                # Feature specs (generated, not hand-written)
│   └── templates/
├── docs/                # System guide, brainstorms, archive
├── tasks/               # todo.md and lessons.md
├── CLAUDE.md            # This file
└── INITIAL.md           # Feature request template
```

---

## Workflow Orchestration

### Plan First
For any task touching more than one file or requiring architectural decisions:
1. Enter plan mode. Read relevant files. Write out the steps.
2. Check in before writing code.
3. Execute the approved plan. Flag any deviations before making them.

### Subagent Strategy
- Use subagents to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- One task per subagent — focused execution only

### Self-Improvement Loop
- After any correction: update `tasks/lessons.md` with the pattern
- Write rules that prevent the same mistake from happening again
- Review `tasks/lessons.md` at the start of each relevant session

### Verification Before Done
A task is ONLY complete when all three pass:
- `pytest` exits 0
- `ruff check .` exits 0
- `mypy src/` exits 0

Report the output of all three before saying you're finished. Never mark a task complete without proving it works.

---

## Task Management
For any task with more than 3 steps:
1. Write the plan to `tasks/todo.md` with checkable items
2. Check in before starting implementation
3. Mark items complete one at a time — never batch
4. Add a review section to `tasks/todo.md` when done
5. Update `tasks/lessons.md` after any correction

---

## Autonomy Boundary

**Auto-proceed:**
- Adding or editing ingestion, scoring, and synthesis logic
- Writing tests and evals
- Fixing lint or type errors
- Refactoring within a single file

**Ask first:**
- Adding new data sources or external API integrations
- Adding new dependencies
- Deleting files
- Any change touching more than 5 files
- Schema changes to the database

**Never:**
- Commit API keys, secrets, or credentials
- Push to main without explicit confirmation
- Store personal email content in version control

---

## Core Principles
- **Simplicity first.** Make every change as simple as possible. No over-engineering.
- **No laziness.** Find root causes. No temporary fixes. Senior engineer standards.
- **Minimal impact.** Only touch what the current task requires.
- **When corrected:** update `tasks/lessons.md` before continuing.
