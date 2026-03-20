# /research

Deep-read the relevant codebase area before writing INITIAL.md or a PRP. Produces a `research.md` file you review and correct before any planning begins.

## Usage
```
/research [area or feature to understand]
```

## When to Run

Before writing INITIAL.md for any non-trivial feature — especially anything that:
- Touches multiple systems or agents
- Changes the database schema
- Requires understanding how existing code works before specifying new behavior
- Is ambiguous enough that wrong assumptions in the plan would be costly

Skip for simple, well-understood tasks.

---

## What This Command Does

1. Deep-reads all files relevant to the area specified
2. Traces data flow, dependencies, and integration points
3. Identifies existing patterns being used
4. Surfaces constraints and non-obvious behaviors
5. Writes findings to `docs/research/[feature]-research.md`

---

## Output Format (written to docs/research/[feature]-research.md)

```markdown
# Research: [feature area]
Date: YYYY-MM-DD

## What I Read
- [files read and why]

## How the Current System Works
[Accurate description of the relevant existing behavior]

## Key Integration Points
[Where the new feature connects to existing code]

## Existing Patterns to Follow
[Patterns found in the codebase that the new feature should use]

## Constraints Discovered
[Non-obvious limitations, gotchas, or dependencies]

## Assumptions I'm Making
[Things not clear from the code — needs human confirmation]

## Open Questions for INITIAL.md
[Specific questions to resolve before planning]
```

---

## After This Command

1. You read `docs/research/[feature]-research.md`
2. Correct any wrong assumptions inline
3. Answer the open questions
4. Then write `INITIAL.md` using the research as input

This is the checkpoint between "figuring out what exists" and "specifying what to build."
