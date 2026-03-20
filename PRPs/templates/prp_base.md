# PRP: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** Draft | Ready | In Progress | Complete

---

## Objective

[One clear sentence describing what this PRP delivers.]

---

## Context

### Problem Being Solved
[Why does this need to exist? What breaks without it?]

### Scope
**In scope:**
- [Item]

**Out of scope:**
- [Item]

### Dependencies
- [Any features or infrastructure that must exist first]

---

## Technical Blueprint

### Stack
- [Framework, version]
- [Database]
- [AI/Agent layer]

### Data Model
```sql
-- Key tables and relationships
```

### Agent Interfaces
```
Agent: [Name]
Pattern: [ReAct | Plan-and-Execute | Multi-Agent]
Input: [What triggers it, what data it receives]
Tools: [List of tools it calls]
Output: [What it produces, where it writes it]
```

### File Structure
```
[Show the files that will be created or modified]
```

### Key Implementation Details
[Anything architecture-level that constrains implementation]

---

## Phase Breakdown

### Phase 1: [Name]
**Goal:** [What this phase delivers]
**Files:** [Files created/modified]
**Validation:**
```bash
[Commands to verify this phase is complete]
```

### Phase 2: [Name]
[Repeat structure]

---

## Validation Gates

All three must pass before any phase is marked complete:
```bash
npm run build       # exit 0
npm run lint        # exit 0
npm run typecheck   # exit 0
```

Agent-specific validation:
```bash
cd agents && pytest # exit 0
```

---

## Open Questions

- [Any unresolved decisions that need to be made during implementation]
