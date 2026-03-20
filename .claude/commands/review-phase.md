# /review-phase

Run a fresh-context code review on the current phase output. Uses the Writer/Reviewer pattern — reviews from an unbiased perspective, separate from the session that built it.

## Usage
```
/review-phase [phase-name or files to review]
```

## When to Run

Run at the end of each major phase, before proceeding to the next. Do NOT run in the same session that built the code — start a new session or use a subagent.

---

## What This Review Covers

### 1. Architecture
- Does this phase's implementation align with the PRP's technical blueprint?
- Are the right patterns from `examples/` being followed?
- Does this create any structural problems for future phases?
- Is there anything that will be painful to change later?

### 2. Code Quality
- Is anything more complex than it needs to be?
- Is there duplication that should be abstracted?
- Are naming conventions consistent with the rest of the codebase?
- Are there obvious edge cases not handled?

### 3. Security
- Are there any injection vulnerabilities (SQL, command, prompt)?
- Is user input validated at system boundaries?
- Are secrets handled correctly (no hardcoded values)?
- Are API routes protected appropriately?

### 4. Agent-Specific (if reviewing agent code)
- Do tool functions return strings (not dicts)?
- Are all HTTP calls async (httpx not requests)?
- Is error handling structured and recoverable?
- Are tool results properly serialized before returning?

### 5. Database (if reviewing schema or queries)
- Are there missing indexes on frequently queried columns?
- Are foreign key constraints correct?
- Is row-level security configured if needed?
- Are migrations safe to run on a live database?

---

## Output Format

```
## Phase Review: [phase name]

### Passed ✓
- [things that are correct and should be kept]

### Issues Found
**Critical (must fix before next phase):**
- [issue]: [why it matters] → [recommended fix]

**Moderate (fix soon, not blocking):**
- [issue]: [why it matters] → [recommended fix]

**Minor (low priority):**
- [issue]: [why it matters] → [recommended fix]

### Patterns to Add to examples/
- [file/pattern]: [why it's worth preserving]

### Lessons to Add to tasks/lessons.md
- [pattern or anti-pattern discovered]
```

---

## Instructions for Claude

When this command is run, treat it as a fresh review with no loyalty to how the code was written. Your job is to find problems, not to confirm the implementation is fine. If something is wrong, say so clearly and specifically. Do not soften findings.

After the review is complete, the user decides which issues to address before proceeding.
