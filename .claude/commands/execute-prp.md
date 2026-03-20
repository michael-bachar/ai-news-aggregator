# /execute-prp

Execute a PRP phase by phase using the Ralph Loop — implement, validate, fix, repeat until all gates pass. Do not stop until every phase is complete and every gate is green.

## Usage
```
/execute-prp PRPs/[feature-name].md
```

---

## Pre-Execution Checklist

Before writing a single line of code:

1. Read the full PRP
2. Read `tasks/lessons.md` — apply all recorded patterns and anti-patterns
3. Read `examples/` — understand the patterns to follow
4. Read `tasks/todo.md` — understand what phase we're on
5. Confirm understanding of the plan with the user before starting

---

## The Ralph Loop (per phase)

For each phase in the PRP:

```
IMPLEMENT → VALIDATE → PASS? → yes → COMPOUND → next phase
                  ↓
                  no
                  ↓
              DIAGNOSE ROOT CAUSE
                  ↓
                FIX IT
                  ↓
              VALIDATE AGAIN
                  ↓
            (loop until pass)
```

**Rules for the loop:**
- Never proceed to the next phase until the current phase passes all gates
- Never patch around a failure — diagnose and fix the root cause
- Never mark a phase complete without running the validation commands
- If the same failure appears 3 times, stop and report — don't loop indefinitely

---

## Validation Gates (run after every phase)

```bash
npm run build       # must exit 0
npm run lint        # must exit 0
npm run typecheck   # must exit 0
```

For agent phases:
```bash
cd agents && pytest # must exit 0
```

---

## COMPOUND Step (after each phase passes)

After a phase passes all validation gates, before moving to the next phase:

1. **Update `tasks/todo.md`** — mark the phase complete, note what was built
2. **Update `examples/`** — if this phase introduced a new pattern that future phases should follow, extract it into `examples/`. Name it clearly (e.g., `examples/agents/base_agent.py`, `examples/api/route.ts`)
3. **Update `tasks/lessons.md`** — if any validation failure occurred and was fixed, document: what failed, why it failed, what the fix was, and the rule to prevent recurrence
4. **Update `CLAUDE.md`** — only if a structural convention changed that applies to all future sessions

---

## Between-Phase Report Format

After each phase, output:

```
✓ Phase [N]: [Name] — COMPLETE
  Validation: build ✓ | lint ✓ | typecheck ✓
  Files created: [list]
  Files modified: [list]
  Pattern added to examples/: [yes/no — which file]
  Lesson recorded: [yes/no — what]

→ Next phase: [N+1]: [Name]
```

---

## Completion Signal

When all phases are complete:

```
✓ PRP COMPLETE: [feature name]
✓ build passing
✓ lint passing
✓ typecheck passing

Phases completed: [list]
Total files created: [N]
Total files modified: [N]
Examples added: [list]
Lessons recorded: [N]
```

---

## If You Hit a Blocker

Stop and report rather than assuming. Do not invent solutions to problems outside the PRP scope. Format:

```
BLOCKER: [what the blocker is]
Context: [what I was doing when I hit it]
Options: [what I see as possible paths forward]
Recommendation: [which path I'd take and why]
Waiting for: [decision needed from user]
```
