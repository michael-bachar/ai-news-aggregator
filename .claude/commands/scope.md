# /scope

Five quick questions to determine whether a feature is simple or complicated, and which path to take. Run this when you're not sure where to start.

## Usage
```
/scope
```

## Instructions for Claude

Ask these five questions using AskUserQuestion, one at a time:

1. "Describe the feature in one sentence. What does it do?"

2. "Does this touch the database schema — adding tables, columns, or changing relationships?"

3. "Does this involve any agent code — Python, Claude API calls, or multi-step automated processing?"

4. "Do you know how this connects to what's already built, or are you uncertain how the pieces fit together?"

5. "Does this depend on something that doesn't exist yet — a table, an API route, another feature?"

---

After the five answers, output a clear verdict:

## SIMPLE PATH ✓
Use this format if:
- No schema changes
- No agent code
- User is clear on how it connects
- No unbuilt dependencies

```
This is a SIMPLE feature.

Start here: /interview
That's all you need. The interview will generate INITIAL.md,
then /generate-prp → annotate PRP → /execute-prp → /review-phase.
```

## COMPLICATED PATH ✓
Use this format if any of the following are true:
- Schema changes involved
- Agent code involved
- User is uncertain how pieces connect
- Unbuilt dependencies

```
This is a COMPLICATED feature.

Recommended path:
[✓ or —] /ce:brainstorm first — [only if: user wasn't sure what they want]
[✓ or —] /research first     — [only if: user uncertain how pieces connect]
         → /interview         — when you're ready to specify
         → /generate-prp
         → annotate PRP (plan for 2-3 rounds)
         → /execute-prp
         → /review-phase per phase

Why complicated: [specific reason based on their answers]
```

Be direct. One verdict, one path. Do not hedge.
