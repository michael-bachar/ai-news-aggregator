---
date: 2026-03-22
topic: mental model for building with AI
---

## Lesson
Building with AI has three phases — before, build, and after — and most mistakes happen because you skip the bookends.

## What happened
I had a V1 pipeline running and was thinking about what to build next. I noticed that `examples/` was empty, `evals/` was untouched, and `tasks/lessons.md` had no entries — even though the system was designed around all three. I had been focusing entirely on the build phase and skipping the steps that make the next build better.

## Why it matters
The build phase (brainstorm → plan → generate → execute) feels like the work. The bookends feel like overhead. But they're actually the compound interest. Without them, every new feature starts from scratch. With them, each feature makes the next one faster and more accurate.

**Before building — two questions:**
- Do I have examples of what good looks like? (`examples/`)
- Do I know what "better" means for this feature? (`evals/`)

**After building — three things:**
- What did I learn? (`tasks/lessons.md`)
- What pattern should future features follow? (`examples/`)
- Did a rule change? (`CLAUDE.md`)

Two other things worth remembering:

**The annotation cycle.** Between "AI writes the plan" and "AI builds the code," there's a step where you open the plan in your editor and add inline notes. This is where your domain knowledge enters. Skip it and you get code that technically works but doesn't fit how you think. 10 minutes here cuts rework by half.

**Scope discipline.** "And it should also..." is where projects die. The AI will build everything you describe. The most important skill is saying "not in this version" before building starts.

## LinkedIn draft
Most people think building with AI is about prompting.

It's not. It's about the bookends.

The build phase — planning, generating, executing — that's the exciting part. But the work that actually compounds happens before and after.

Before you build anything:
- Do you have examples of what good looks like?
- Do you know how you'll measure success?

After you finish:
- What did you learn that you don't want to re-learn?
- What pattern should the next feature follow?

Skip these and every feature starts from scratch. Do them consistently and each build makes the next one faster.

The other thing nobody talks about: the annotation cycle. Between "AI writes the plan" and "AI writes the code," there's a step where you open the plan and add your own notes inline. That's where your knowledge enters. Without it, the AI builds what it thinks you want.

And scope discipline. The AI will build everything you describe. "And it should also..." is where projects die. The skill is saying "not in this version" before building starts.

Building with AI is a compound skill. The people getting the most out of it aren't just better at prompting — they're better at the parts around the prompting.
