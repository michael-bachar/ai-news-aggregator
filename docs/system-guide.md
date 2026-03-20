# How This System Works

A guide for both human contributors and AI coding agents. Explains the file structure, the build process, the mental model, and how to use everything correctly.

**Last updated:** March 8, 2026
**Rooted in:** Boris Cherny (Claude Code creator), Boris Tane, coleam00/context-engineering-intro, Wirasm/PRPs-agentic-eng, Martin Fowler, Anthropic official docs, Andrej Karpathy field notes, arxiv context engineering paper (Feb 2026).

---

## The Core Problem This Solves

The bottleneck in AI-assisted development is not the AI's ability to write code. It's context. Every session starts blank. The AI doesn't know your architecture decisions, your conventions, what you tried last week, or why you made the choices you did. Without structured context, it drifts — reinventing patterns, making assumptions, producing code that technically works but doesn't fit the system.

**This entire file structure is the solution.** Every file gives the AI exactly the right context at exactly the right time, without overloading the context window with noise.

The arxiv context engineering paper (Feb 2026) studied 283 sessions across 70 days building a 108,000-line codebase. Structured context files reduced AI runtime by **29%** and output token consumption by **17%**. That's the difference between an AI that drifts and one that stays on course.

---

## The Mental Model

Everything runs through one loop with six phases:

```
UNDERSTAND → SPECIFY → ALIGN → BUILD → VERIFY → COMPOUND
     ↑                                                |
     └────────────────────────────────────────────────┘
```

Every cycle through this loop makes the next one faster and more accurate. This is compound engineering.

### UNDERSTAND
Before writing anything, make sure both you and the AI deeply understand the problem and the relevant codebase. For simple features, the brainstorm is enough. For complex features, run `/research` first — the AI deep-reads the relevant code and writes a `research.md` file you review and correct before any planning begins.

**Tools:** `/ce:brainstorm`, `/research`

### SPECIFY
Translate understanding into a structured brief (INITIAL.md), then let the AI generate the full technical blueprint (PRP). The PRP includes the data model, agent interfaces, file structure, phase breakdown, and validation gates.

**Tools:** Fill `INITIAL.md` → `/generate-prp`

### ALIGN
Not a passive read. Open the PRP in your editor. Add inline correction notes directly into the document. Send it back with "address all notes, don't implement yet." Repeat 1–3 times until it's solid. This is where your domain knowledge enters the plan. A passive review misses this entirely.

**The explicit guard:** "Don't implement yet" prevents the AI from jumping ahead before the plan is right.

### BUILD
Autonomous execution with continuous validation — the Ralph Loop. The AI implements, runs all validation gates, fixes failures at the root cause, and re-validates. It does not ask for help on failures. It does not proceed until the current phase passes. It does not patch around problems.

**Tools:** `/execute-prp`

### VERIFY
Fresh-context review at the end of each phase. Not the AI reviewing its own work in the same session — that's anchored to its own reasoning and misses things. A new context catches what the author missed. This is the Writer/Reviewer pattern.

**Tools:** `/review-phase` (run in a new session or as a fresh subagent)

### COMPOUND
After every phase — explicit, named steps, not implied:
1. Update `tasks/lessons.md` — what failed, why, what the fix was, what rule prevents recurrence
2. Update `examples/` — if a novel pattern was introduced that future phases should follow, extract it
3. Update `CLAUDE.md` — only if a structural convention changed that applies to all future sessions

---

## The File Structure

```
your-project/
├── CLAUDE.md                         # Project constitution — always loaded, <100 lines
├── .claudeignore                     # Blocks irrelevant files from context
├── README.md                         # Human-facing front door — GitHub audience
├── INITIAL.md                        # Feature request template — input to /generate-prp
├── .claude/
│   ├── commands/
│   │   ├── research.md               # /research — deep-read before INITIAL.md
│   │   ├── generate-prp.md           # /generate-prp — PRP from INITIAL.md
│   │   ├── execute-prp.md            # /execute-prp — Ralph Loop build
│   │   └── review-phase.md          # /review-phase — Writer/Reviewer fresh review
│   └── settings.local.json           # Pre-allowed bash commands
├── PRPs/                             # Product Requirements Prompts — what the AI builds from
│   ├── templates/prp_base.md         # Reusable PRP structure
│   └── [feature-name].md             # Feature-specific implementation blueprints
├── examples/                         # Code patterns — updated after each phase explicitly
├── docs/
│   ├── system-guide.md               # ← this file
│   ├── research/                     # research.md files from /research command
│   ├── brainstorms/                  # Reasoning behind decisions, pre-PRP
│   └── archive/                      # Old PRDs and deprecated docs
└── tasks/
    ├── todo.md                       # Active phase checklist
    └── lessons.md                    # Compound engineering loop — mistakes become rules
```

---

## Each File and Folder Explained

### `CLAUDE.md` — The Project Constitution

Read automatically at the start of every session. Checked into git. Shared across sessions.

Boris Cherny's team updates their CLAUDE.md multiple times per week. When a reviewer spots an anti-pattern in a PR, they update CLAUDE.md — not just leave a comment. Anti-patterns become rules permanently encoded into future behavior. This is **compound engineering**.

**What goes in it:**

| Include | Exclude |
|---|---|
| Commands the AI can't guess | Standard conventions it already knows |
| Architecture decisions specific to this project | Long explanations (link instead with `@path/to/file`) |
| Three-tier autonomy boundary (auto / ask first / never) | Anything that changes frequently |
| Non-obvious gotchas | File-by-file codebase descriptions |

**Golden rule:** For every line, ask "would removing this cause the AI to make mistakes?" If not, cut it. Target under 100 lines. Bloated CLAUDE.md files cause the AI to ignore actual rules because signal is buried in noise.

**Import syntax:** Use `@path/to/file` to reference other documents without duplicating content:
```markdown
See @docs/system-guide.md for the full build process.
Read @tasks/lessons.md before implementing anything.
```

---

### `.claudeignore` — Context Blocker

Blocks irrelevant files from being read during research and PRP generation. Without this, the AI wastes significant context on `node_modules/`, `.next/`, lock files, and build artifacts.

Create this before any other work. Every file path listed here is invisible to the AI during codebase exploration.

---

### `INITIAL.md` — Feature Request Template

Fill this out before running `/generate-prp`. Four sections:
1. **FEATURE** — what it does, who triggers it, expected output, success criteria
2. **EXAMPLES** — references to `examples/` folder patterns to follow
3. **DOCUMENTATION** — links to APIs and libraries the AI should fetch and read
4. **OTHER CONSIDERATIONS** — constraints, edge cases, what not to do

This is the alignment layer. It's what you and the AI commit to before any technical work begins. Structured input → structured output.

---

### `PRPs/` — Product Requirements Prompts

**The most important folder.** A PRP is the document the AI actually builds from.

**PRP vs PRD:**

| PRD (for human engineers) | PRP (for AI agents) |
|---|---|
| What and why | What, why, AND how |
| Avoids implementation details | Includes exact file paths, library versions, code examples |
| No validation mechanism | Includes executable commands to verify work |
| Static document | Active runbook with validation loops |

From Wirasm/PRPs-agentic-eng: "A PRP is the minimum viable packet an AI needs to ship production-ready code on the first pass."

`templates/prp_base.md` is the reusable structure. Each feature gets its own PRP file in `PRPs/`.

---

### `.claude/commands/` — Slash Commands

Custom commands run inside Claude Code sessions. Checked into git — anyone who clones the repo gets them.

**`/scope`**
Five quick questions that output a clear verdict: **SIMPLE PATH** (go straight to `/interview`) or **COMPLICATED PATH** (do brainstorm and/or research first, with specific recommendations). Run this when you're not sure where to start.

**`/research [area]`**
For complex features: deep-reads the relevant codebase area and writes findings to `docs/research/[feature]-research.md`. You review and correct it before writing INITIAL.md. Catches wrong assumptions before they contaminate the plan.

**`/interview`**
The entry point for specifying any feature. Interviews you with structured questions one at a time (using AskUserQuestion), then generates a completed INITIAL.md from your answers. Has built-in routing: if you can't answer the core feature question clearly, it pauses and routes you to `/ce:brainstorm`; if you can't answer data/integration questions, it pauses and routes you to `/research`. This means `/interview` is self-correcting — you don't need to know in advance whether you need brainstorm or research.

**`/generate-prp INITIAL.md`**
Reads the feature brief, explores the codebase, fetches documentation links, looks at `examples/`, and produces a complete PRP — technical blueprint, data model, agent interfaces, phase breakdown, validation gates.

**`/execute-prp PRPs/[feature].md`**
The Ralph Loop: read PRP → confirm plan → implement phase → validate all gates → if failing: diagnose root cause, fix, re-validate → proceed only when passing → COMPOUND step → next phase. Autonomous. Does not ask for help on failures.

**`/review-phase [files]`**
Writer/Reviewer pattern: fresh-context review covering architecture, code quality, security, agent patterns, and database safety. Run at the end of each phase in a new session or as a fresh subagent — not in the same session that built the code.

---

### `examples/` — Code Patterns

Working code the AI patterns against when writing new code.

coleam00 (canonical context engineering reference): "The examples folder is critical for success." When no examples exist, the AI invents patterns. With good examples, it follows them consistently — keeping the codebase coherent across many sessions and many features.

**Starts empty. Updated explicitly after every phase.** After a phase passes validation, any novel pattern introduced goes into `examples/`. This is not implied — it's a named step in the COMPOUND phase. Examples added here make every future PRP more accurate.

---

### `docs/research/` — Pre-Planning Research

Produced by `/research`. Contains the AI's deep-read findings for a specific codebase area before planning begins. You review these, correct wrong assumptions, and then write INITIAL.md using the research as input.

Skip for simple features. Essential for anything touching multiple systems or requiring accurate understanding of existing behavior.

---

### `docs/brainstorms/` — Session Reasoning

Captures the reasoning behind decisions before code is written. What did we consider? What did we reject and why? What are the trade-offs?

Separate from PRPs: brainstorms capture the why. PRPs capture the how. If you need to understand a decision six months later, the brainstorm is where you look.

---

### `tasks/todo.md` — Active Checklist

Organized by PRP phase. Each phase is a section. Each file or task within that phase is a checkbox. The AI updates this as part of executing — you don't manage it manually.

---

### `tasks/lessons.md` — Compound Engineering Loop

Every mistake, every correction, every discovered constraint, every confirmed pattern goes here.

Boris Cherny: "When a reviewer spots an anti-pattern in a PR, they tag @claude to update the rules. Anti-patterns get encoded as rules, not left as comments."

`tasks/lessons.md` is this loop in document form. Three categories:
- **Anti-patterns** — things that broke, failed validation, or produced wrong output
- **Patterns** — things that worked and should be repeated
- **Constraints** — things discovered mid-build that weren't in the PRP

**Updated after every phase as an explicit COMPOUND step** — not implied, not optional.

---

## Compound Engineering Skills vs Project Commands

These are two different layers that work together, not competing tools.

| Layer | Examples | When to Use |
|---|---|---|
| **Compound engineering skills** | `/ce:brainstorm`, `/ce:review` | Open-ended reasoning — figuring out what to build, architectural exploration, meta-level review |
| **Project commands** | `/research`, `/generate-prp`, `/execute-prp`, `/review-phase` | Repeatable project workflow — the build loop |

**In practice:**
- Use `/ce:brainstorm` when you don't know what you're building yet
- Use `/ce:plan` only when architectural questions remain unresolved after brainstorming (otherwise skip — `/generate-prp` handles it)
- Use project commands for everything in the build loop
- Use `/review-phase` (project command) for phase-level code review; `/ce:review` for broader architectural sessions

The compound engineering skills are the bookends — before (brainstorm) and occasionally after (meta review). Project commands are the middle — the actual build loop.

---

## How to Know Where to Start

**`/interview` is always the entry point for specifying a feature.** The question is whether you need to do anything before it.

```
Unsure where to start?
  → /scope         (5 questions → clear SIMPLE or COMPLICATED verdict)

SIMPLE PATH (no schema, no agent code, clear scope, no missing deps):
  → /interview → done

COMPLICATED PATH (schema changes, agent code, uncertain connections, unbuilt deps):
  → /ce:brainstorm   ← only if: "I don't know what I want yet"
  → /research        ← only if: "I don't know how existing code connects"
  → /interview → done
```

**`/interview` also self-corrects.** If you start it and realize mid-interview that you don't know what you want, or don't know what already exists — the interview pauses and tells you which pre-step to run. You don't need to predict this in advance.

The three entry questions that tell you what to do:
1. "Do I know what I want to build?" → No → `/ce:brainstorm` first
2. "Do I know how this connects to what's built?" → No → `/research` first
3. Both yes → `/interview` directly

---

## The Full Workflow

```
/ce:brainstorm [optional]   ← only if: unclear what to build
      ↓
/research [optional]        ← only if: unclear how existing code connects
      ↓
/interview                  ← entry point → generates INITIAL.md
      ↓
/generate-prp               ← AI produces full technical blueprint
      ↓
Annotation cycle            ← open PRP, add inline notes, "address notes, don't implement yet"
  (repeat 1-3x)             ← iterate until solid
      ↓
/execute-prp                ← Ralph Loop: implement → validate → fix → validate → proceed
  (per phase)
      ↓
/review-phase               ← fresh-context review at end of each phase
      ↓
COMPOUND                    ← tasks/lessons.md + examples/ + CLAUDE.md (explicit, named)
      ↓
Next phase or next feature → repeat
```

---

## The Validation Gate (non-negotiable, every phase)

```bash
npm run build       # must exit 0
npm run lint        # must exit 0
npm run typecheck   # must exit 0
cd agents && pytest # must exit 0 (agent phases)
```

A phase is ONLY complete when all gates pass. The AI does not proceed, does not batch phases, does not mark anything done without proving it works.

---

## Task Tracking

**Now:** `tasks/todo.md` — in the repo, visible to the AI every session, updated during execution.

**When to move to Linear:**
- More than one contributor
- Multiple parallel workstreams
- Need issue history for external GitHub contributors

Keep task tracking inside the repo for the AI. Linear or Jira is for you.

---

## Day-to-Day Session Discipline

**Starting a session:**
1. AI reads `CLAUDE.md` automatically
2. Read `tasks/lessons.md` — apply all patterns and anti-patterns
3. Read `tasks/todo.md` — what phase are we on, what's next
4. Open the active PRP — what are we building

**During a session:**
- Work against the current phase in the PRP
- Ralph Loop: implement → validate → fix → re-validate
- Never proceed past a failing gate
- If the same failure appears 3 times without resolution, stop and report

**Ending a session:**
- Update `tasks/todo.md` — mark completed, note what's next
- COMPOUND: update `tasks/lessons.md`, `examples/`, `CLAUDE.md` if needed
- Name the session if multi-day work (`/rename feature-phase-1`)

**Between sessions:**
- CLAUDE.md should reflect any new rules discovered
- `examples/` should have any new patterns extracted
- `tasks/lessons.md` should have any mistakes encoded

---

## What Beginners Miss (from research across 10+ practitioner sources)

1. **The annotation cycle** — passive PRP review misses the point. Inline notes + iteration is where domain knowledge enters the plan.
2. **`.claudeignore`** — without it, the AI reads node_modules and .next and wastes context.
3. **`examples/` as an explicit step** — it doesn't fill itself. It needs a named update after each phase.
4. **Writer/Reviewer isolation** — same-session review is anchored to the author's reasoning. Fresh context finds different things.
5. **`/research` before complex features** — jumping from brainstorm to INITIAL.md skips understanding the existing system.
6. **`lessons.md` after every phase, not just corrections** — patterns (positive) matter as much as anti-patterns.
7. **CLAUDE.md pruning** — rules accumulate. Periodically ask "does removing this cause mistakes?" If not, cut it.

---

## What You Need to Know vs. What Claude Handles

A common misconception when starting out: the workflow requires you to have all the technical answers. It doesn't. Here's the actual split.

**Your job — product decisions. Only you can make these:**

| You provide | Why Claude can't |
|---|---|
| What outcome do we want? | It doesn't know your goals |
| What's in scope for v1? | It will build everything if you let it |
| What does "done" look like? | It needs a success definition |
| What are the business rules? | "A prep session is per interview, not per day" — that's a product call |

**Claude's job — technical decisions. Claude discovers and handles these:**

| Claude figures out | How |
|---|---|
| What tables exist | `/research` reads the schema |
| What patterns are already in use | `/research` reads the codebase |
| What migration is needed | Derived from your outcome description |
| How to connect to the API | It knows the patterns |
| What files to change | It maps this from the feature description |

**`/research` specifically flips the dynamic.** You don't need to know how the existing code works before the interview. Run `/research` first — Claude reads the codebase and tells you what's there. You review and correct it. Then the interview asks product questions you can actually answer, informed by what Claude found.

### The Four Things You Do Need to Develop

Not how to write SQL, Python, or TypeScript. Conceptual vocabulary — the ability to think in the right units.

**1. What is data?**
Tables store things. An "interviews" table has rows. Adding a new thing (like prep sessions) requires a new table. Changing what a row contains requires a migration. You don't write this — you just need to recognize "this is a new thing, so it probably needs a new table."

**2. What is a boundary?**
Some logic lives in the browser, some on the server, some in the database, some in an external API. Knowing roughly which layer a feature touches tells you whether it's a simple page or a complicated system integration.

**3. What is an agent vs. a function?**
A function does one thing and stops: fetch interviews, display them. An agent reasons in a loop: look at this interview, generate questions, search stories, identify gaps, decide what to surface. If the feature involves decisions and iteration, it's probably an agent.

**4. What is scope creep?**
The instinct to say "and it should also..." is where projects die. This is a PM skill, not a technical one. You already have it.

### The PM Advantage

Engineers often struggle with the interview step. They want to jump to implementation. They under-specify success criteria. They resist saying "this is NOT in scope."

PMs are trained to do exactly what the interview asks: define outcomes, bound scope, specify success, identify trade-offs. That's your job description, and it maps directly to what the workflow needs from you.

The gap to close isn't technical. It's product clarity — knowing what you want precisely enough that Claude can execute it. That comes with reps, not with learning to code.

### Why Experts Seem Faster

They have product pattern recognition, not more technical knowledge. They've shipped enough things to immediately know "v1 doesn't need filtering" without deliberating. They can answer the interview questions in ten minutes because they've seen the same decisions before.

The speed comes from having made the same product trade-offs repeatedly, not from knowing what database tables to use.

---

## The Single Most Important Principle

From Boris Cherny, Karpathy, Boris Tane, the arxiv paper, and every source in the research:

**The quality of what the AI builds is directly proportional to the quality of the context you give it.**

A vague request gets vague code. A well-annotated PRP, with real examples, executable validation gates, and an active COMPOUND loop gets production-quality code that compounds in quality with every session.

---

---

## Step-by-Step: How to Actually Use This System

### The Basics — How Claude Code Works

Run Claude Code from your project directory:
```bash
cd /path/to/job-search-agent
claude
```

This opens an interactive session. It reads `CLAUDE.md` automatically. Slash commands are typed directly in the chat (`/generate-prp INITIAL.md`). Compound engineering skills work the same way (`/ce:brainstorm`).

**Parallel instances:** Open multiple terminal tabs. Run `claude` in each. They are fully independent — different context windows, no shared state. Switch between tabs like browser windows.

---

### Simple Feature Flow

**When to use:** One clear thing to build, you know what it is, touches 1–3 files, no schema uncertainty, no complex agent interactions.

**Example:** "Add a story bank view page showing all stories with deployment count."

```
Tab 1: Main build session (stays open the whole feature)
Tab 2: Review session (opened fresh per phase, then closed)
```

**Step 1 — Open Tab 1**
```bash
claude
```

**Step 2 — Create INITIAL.md**
Two ways to do this:

*Option A — Interview (recommended):* Let Claude ask you questions one at a time and generate INITIAL.md from your answers:
```
/interview
```

*Option B — Write it yourself:* Open `INITIAL.md` in your editor and fill in all four sections manually. Better when you already have everything fully articulated.

**Step 3 — Generate the PRP**
```
/generate-prp INITIAL.md
```
Claude researches the codebase, fetches your docs links, produces `PRPs/[feature].md`. Takes 2–5 minutes.

**Step 4 — Annotate the PRP** (in your editor)
Open the PRP. Add inline notes where anything is wrong:
```markdown
<!-- NOTE: Use shadcn/ui Card, not a custom card -->
```
Back in Tab 1:
```
I've annotated PRPs/[feature].md. Address all notes. Do not implement yet.
```
One round is usually enough for a simple feature.

**Step 5 — Execute**
```
/execute-prp PRPs/[feature].md
```
Claude confirms the plan, waits for your go-ahead, then runs the Ralph Loop per phase: implement → validate → fix → validate → proceed.

**Step 6 — Review (Tab 2, fresh)**
When a phase completes, open a new terminal tab:
```bash
claude
```
```
/review-phase app/stories/page.tsx components/story-card.tsx
```
Bring critical findings back to Tab 1, fix, then close Tab 2.

**Step 7 — COMPOUND**
```
Phase complete. Update tasks/todo.md, extract new patterns into examples/,
update tasks/lessons.md with any failures.
```

**Total tabs:** 2. Total context switches: once per phase for review.

---

### Complicated Feature Flow

**When to use:** Multiple systems involved, schema decisions need to be right first time, involves agent code, you're not sure how pieces connect.

**Example:** "Build the Prep Agent — decomposes an upcoming interview into tasks, pulls questions, matches stories, checks gaps, outputs a briefing."

```
Tab 1: Main build session (full feature)
Tab 2: Review session (fresh per phase) OR research session (while Tab 1 executes)
```

**Step 1 — Brainstorm (Tab 1)**
```
/ce:brainstorm
```
Answer the questions it asks. At the end:
```
Save this to docs/brainstorms/YYYY-MM-DD-[feature].md
```

**Step 2 — Research (Tab 1)**
```
/research agents prep-agent question-bank stories database-schema
```
Claude deep-reads the relevant codebase, produces `docs/research/[feature]-research.md`.

Open that file in your editor. Correct wrong assumptions inline:
```markdown
<!-- CORRECTION: Questions are stored as JSONB, not plain text -->
```
Back in Tab 1:
```
I've corrected docs/research/[feature]-research.md. Read it before we proceed.
```

**Step 3 — Write INITIAL.md** (in your editor)
Now you write it with full understanding of what exists. Much more precise than writing cold.

**Step 4 — Generate the PRP (Tab 1)**
```
/generate-prp INITIAL.md
```

**Step 5 — Deep Annotation Cycle** (2–3 rounds)
Open PRP in your editor. Annotate. Back in Tab 1:
```
Annotated PRPs/[feature].md. Address all notes. Do not implement yet.
```
Re-read. Annotate again if needed. Repeat until solid.

Before starting execution, explicitly confirm:
```
Confirm your understanding of Phase 1 before we start.
```
Claude summarizes. If it matches your intent, proceed.

**Step 6 — Execute with Parallel Research (Tab 1 + Tab 2)**
```
/execute-prp PRPs/[feature].md
```
While Tab 1 runs Phase 1, open Tab 2 for productive parallel work:
- Look up something you're unsure about
- Read ahead in the PRP for Phase 2 issues
- Draft test data

When Phase 1 completes in Tab 1, close Tab 2.

**Step 7 — Review (Tab 2, fresh)**
Open new Tab 2:
```
/review-phase agents/prep/agent.py agents/prep/tools.py
```
Bring critical findings to Tab 1. Fix. Close Tab 2.

**Step 8 — COMPOUND**
```
Phase 1 complete. Mark done in tasks/todo.md. Extract base agent pattern
into examples/agents/base_agent.py. Update tasks/lessons.md.
```

**Step 9 — Repeat Steps 6–8 for each subsequent phase.**
By Phase 2, `examples/` has patterns from Phase 1. Claude follows them automatically.

---

### When to Use /research

| Use it | Skip it |
|---|---|
| Touches multiple existing systems | Single new component or page |
| Schema decisions that are hard to undo | Simple CRUD route |
| Agent interactions across multiple files | You already know what exists |
| You're unsure how existing pieces connect | Feature is self-contained |

---

### When to Open a Second Tab

| Always | Sometimes | Never |
|---|---|---|
| `/review-phase` — fresh context required | Research while Tab 1 executes | Same work as Tab 1 |
| | Look something up mid-execution | To "watch" Tab 1 |

---

### Quick Reference

```
SIMPLE FEATURE
  Tab 1: claude
    /interview (or write INITIAL.md manually) → /generate-prp → annotate PRP (1 round)
    → /execute-prp → per phase:
  Tab 2 (fresh): /review-phase → findings back to Tab 1
  Tab 1: COMPOUND

COMPLICATED FEATURE
  Tab 1: claude
    /ce:brainstorm → /research → correct research.md
    → /interview (or write INITIAL.md manually) → /generate-prp
    → annotate PRP (2-3 rounds) → confirm plan
    → /execute-prp → per phase:
  Tab 2 (fresh): /review-phase → findings back to Tab 1
  Tab 1: COMPOUND → next phase → repeat

VALIDATION GATE (every phase)
  npm run build       ← exit 0
  npm run lint        ← exit 0
  npm run typecheck   ← exit 0
  cd agents && pytest ← exit 0 (agent phases)

COMPOUND (after every phase)
  tasks/todo.md    ← mark done
  examples/        ← new patterns
  tasks/lessons.md ← failures + patterns learned
  CLAUDE.md        ← only if a rule changed
```

---

## Key Sources

- [Boris Cherny — How the Creator of Claude Code Uses Claude Code](https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually)
- [Boris Tane — Plan Quality Over Execution Speed](https://boristane.com)
- [Anthropic — Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Anthropic — Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic — Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)
- [Wirasm/PRPs-agentic-eng](https://github.com/Wirasm/PRPs-agentic-eng)
- [Martin Fowler — Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- [arxiv — Codified Context: Infrastructure for AI Agents (Feb 2026)](https://arxiv.org/html/2602.20478v1)
- [Andrej Karpathy — Claude Code Field Notes (Jan 2026)](https://dev.to/jasonguo/karpathys-claude-code-field-notes-real-experience-and-deep-reflections-on-the-ai-programming-era-4e2f)
- [Matthew Groff — Implementing CLAUDE.md Agent Skills](https://www.groff.dev/blog/implementing-claude-md-agent-skills)
