# /generate-prp

Generate a comprehensive PRP (Product Requirements Prompt) from an INITIAL.md feature request.

## Usage
```
/generate-prp INITIAL.md
```

## What This Command Does

1. **Read** the INITIAL.md feature request
2. **Explore** the existing codebase for relevant patterns, existing implementations, and constraints
3. **Fetch** any documentation URLs listed in the INITIAL.md
4. **Research** the `examples/` folder for code patterns to follow
5. **Generate** a complete PRP using `PRPs/templates/prp_base.md` as the base

## Output

Creates `PRPs/[feature-name].md` containing:
- Clear objective and scope
- Technical blueprint (data model, agent interfaces, file structure)
- Phase breakdown with milestones
- Validation gates (commands that must pass at each phase)
- Implementation details specific to this codebase

## Instructions for Claude

When this command is run:

1. Ask clarifying questions if INITIAL.md is ambiguous — do not assume
2. Read all files in `examples/` before generating the PRP
3. Read `CLAUDE.md` and existing source files to understand current patterns
4. Fetch all documentation URLs listed in the INITIAL.md
5. Use `PRPs/templates/prp_base.md` as the structure template
6. Be specific about file paths — use actual paths from this codebase, not placeholders
7. Include executable validation commands that actually work for this stack
8. Flag any open questions rather than making assumptions about them
9. Save the output to `PRPs/[kebab-case-feature-name].md`

## Quality Bar

A good PRP should be specific enough that executing it produces working code on the first pass with no ambiguity about what to build.
